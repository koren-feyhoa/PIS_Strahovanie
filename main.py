from contextlib import asynccontextmanager
from datetime import datetime,date
from typing import Dict

from sqlalchemy import update
import pathlib
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import SessionLocal
import CURD
import models
from domain.repositories.sqlalchemy_application_repo import SQLAlchemyApplicationRepository
from domain.repositories.sqlalchemy_client_repo import SQLAlchemyClientRepository
from domain.repositories.sqlalchemy_contract_repo import SQLAlchemyContractRepository
from domain.repositories.sqlalchemy_profile_repo import SQLAlchemyProfileRepository
from domain.services.ApplicationService import ApplicationServise

from domain.services.ClientService import ClientServise
from domain.services.ContractService import ContractService
from domain.services.ProfileService import ProfileService

from fastapi.responses import FileResponse

def update_expired_contracts_status():
    """Функция, которая выполняется по расписанию и обновляет статус договоров"""
    db = SessionLocal()
    try:
        today = date.today()
        stmt = update(models.Contract).where(
            models.Contract.end_date < today,
            models.Contract.status_contract != "Срок действия истёк"
        ).values(status_contract="Срок действия истёк")
        result = db.execute(stmt)
        db.commit()
        if result.rowcount:
            print(f"[INFO] {result.rowcount} договоров обновлено на 'Срок действия истёк'")
    except Exception as e:
        print(f"[ERROR] Ошибка при обновлении: {e}")
        db.rollback()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    update_expired_contracts_status()
    # Этот блок выполняется ПРИ ЗАПУСКЕ приложения
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_expired_contracts_status, 'cron', hour=0, minute=5)
    scheduler.start()
    print("Scheduler started, will run every day at 00:05")
    yield
    # Этот блок выполняется ПРИ ОСТАНОВКЕ приложения
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/test_route")
def test():
    return {"message": "ok"}
@app.post("/client/")
async def createClient(fullname:str,phone:str,email:str,password:str, db: Session = Depends(get_db)):
    repo=SQLAlchemyClientRepository(db)
    service=ClientServise(repo)
    result=await service.create_client(
        fullname=fullname,
        phone=phone,
        email=email,
        password=password
    )
    return result

@app.post("/client/newApplication")
async def createApplication(client_id:int, agent_id:int,insurance_type:str,  profile_id:int , db:Session=Depends(get_db)):
    repo=SQLAlchemyApplicationRepository(db)
    service=ApplicationServise(repo)
    result=await service.create_application(
        client_id=client_id,
        agent_id=agent_id,
        insurance_type=insurance_type,
        profile_id=profile_id,

    )
    return result

@app.get("/client/myApplications")
def getAllUserApplication(id_client: int, db:Session=Depends(get_db)):
    return CURD.getAllUserApplication(db,id_client)

@app.post("/agent/contracts/")
async def create_contract(
    client_id: int ,
    application_id: int,
    agent_id: int ,
    contract_number: str ,
    start_date: date ,
    end_date: date,
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
):
    repo=SQLAlchemyContractRepository(db)
    service=ContractService(repo)
    result = await service.create_contract(
        client_id=client_id,
        application_id=application_id,
        agent_id=agent_id,
        contract_number=contract_number,
        start_date=start_date,
        end_date=end_date,
        file_upload=file,
    )
    return result


@app.get("/contracts/contract")
async def getContract(contract_id:int,client_id:int,db: Session = Depends(get_db)):
    contract=CURD.getContractById(db,contract_id)
    if contract.client_id != client_id:
        raise HTTPException(403, "Access denied")
    file_path=pathlib.Path(contract.file_path)/contract.file_name
    if not file_path.exists():
        raise HTTPException(404, "File not found on server")
    return FileResponse(path=file_path,
        filename=contract.file_name,   # имя, которое увидит пользователь
        media_type="application/octet-stream" )

@app.get("/client/contracts")
async def getContractsByClient(client_id:int,db: Session = Depends(get_db)):
    contracts=CURD.getContractsByClient(db,client_id)
    return contracts

@app.post("/client/application/profiles")
async def createProfile(client_id:int,type_document:str,info:Dict[str,str],db: Session = Depends(get_db)):
    repo=SQLAlchemyProfileRepository(db)
    service=ProfileService(repo)
    result= await service.create_profile(client_id, type_document, info)
    return result

@app.get("/client/application/see_info")
async def getProfileById(id:int,db: Session = Depends(get_db)):
    return CURD.readProdileById(db,id)






