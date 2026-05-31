from contextlib import asynccontextmanager
from dataclasses import asdict
from datetime import datetime,date
from typing import Dict
from fastapi import Body
from sqlalchemy import update
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from domain.entities.ApplicationEntity import ApplicationEntity
from domain.entities.ApplicationUpdate import ApplicationUpdate
from domain.entities.ClientUpdate import ClientUpdate
from domain.entities.ProfileEntity import ProfileEntity
from domain.entities.ProfileUpdate import ProfileUpdate
from domain.repositories.sqlalchemy_agent_repo import SQLAlchemyAgentRepository
from domain.repositories.sqlalchemy_application_repo import SQLAlchemyApplicationRepository
from domain.repositories.sqlalchemy_client_repo import SQLAlchemyClientRepository
from domain.repositories.sqlalchemy_contract_repo import SQLAlchemyContractRepository
from domain.repositories.sqlalchemy_profile_repo import SQLAlchemyProfileRepository
from domain.services.AgentService import AgentServise
from domain.services.ClientService import ClientService
from domain.services.ApplicationService import ApplicationServise
from domain.services.ContractService import ContractService
from domain.services.ProfileService import ProfileService
from domain.services.ApplicationToContractService import ApplicationToContractService

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
    service=ClientService(repo)
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
@app.patch("/client/{client_id}")
async def update_client(client_id: int,
                        update_data: ClientUpdate = Body(...),
                        db: Session = Depends(get_db)):
    repo=SQLAlchemyClientRepository(db)
    service=ClientService(repo)
    updates = {k: v for k, v in asdict(update_data).items() if v is not None}
    if not updates:
        raise HTTPException(400, "No fields to update")
    try:
        updated = await service.update_client(client_id, updates)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return updated

@app.get("/agent/allClients")
async def getAllUsers(db:Session=Depends(get_db)):
    repo=SQLAlchemyAgentRepository(db)
    repo_client=SQLAlchemyClientRepository(db)
    service=AgentServise(repo_client,repo)
    return service.get_all_clients()

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
    repo_app=SQLAlchemyApplicationRepository(db)
    service=ApplicationToContractService(repo,repo_app)
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





@app.post("/client/application/profiles")
async def createProfile(client_id:int,type_document:str,info:Dict[str,str],db: Session = Depends(get_db)):
    repo=SQLAlchemyProfileRepository(db)
    service=ProfileService(repo)
    result= await service.create_profile(client_id, type_document, info)
    return result


@app.get("/agent")
async def getAgentById(id:int,db: Session = Depends(get_db)):
    repo=SQLAlchemyAgentRepository(db)
    client_repo=SQLAlchemyClientRepository(db)
    service=AgentServise(client_repo,repo)
    result= service.get_by_id(id)
    return result
@app.get("/agent/allapp")
async def getAllApplications(db:Session=Depends(get_db)):
    repo=SQLAlchemyApplicationRepository(db)
    service=ApplicationServise(repo)
    result=await service.get_all_applications()
    return result
@app.get("/client/applications")
async def clientApplication(client_id:int,db:Session=Depends(get_db)):
    repo=SQLAlchemyApplicationRepository(db)
    service=ApplicationServise(repo)
    result=await service.get_applications_by_client(client_id)
    return result

@app.patch("/agent/applications/update")
async def updateApplication(application_id:int,
                            updates_data:ApplicationUpdate=Body(...),
                            db:Session=Depends(get_db)):
    repo=SQLAlchemyApplicationRepository(db)
    service=ApplicationServise(repo)
    updates = {k: v for k, v in asdict(updates_data).items() if v is not None}
    if not updates:
        raise HTTPException(400, "No fields to update")
    try:
        updated = await service.update_price_application(application_id, updates)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return updated

@app.patch("/client/applications/{application_id}")
async def rejectApplication(application_id:int, db:Session=Depends(get_db)):
    repo=SQLAlchemyApplicationRepository(db)
    service=ApplicationServise(repo)
    result= await service.update_status_reject(application_id)
    return result

@app.patch("/client/applications/{application_id}/accept")
async def acceptApplication(application_id:int, db:Session=Depends(get_db)):
    repo=SQLAlchemyApplicationRepository(db)
    service=ApplicationServise(repo)
    result= await service.update_status_accept(application_id)
    return result

@app.get("/client/account")
async def get_all_profiles_by_client(client_id:int,db:Session=Depends(get_db)):
    repo=SQLAlchemyProfileRepository(db)
    service=ProfileService(repo)
    result=await service.get_profiles_by_client_id(client_id)
    return result

# @app.patch("/client/account",response_model=ProfileEntity)
# async def update_profile(profile_id:int,
#                          updates_data:ProfileUpdate=Body(...),
#                          db:Session=Depends(get_db))->ProfileEntity:
#     repo=SQLAlchemyProfileRepository(db)
#     service=ProfileService(repo)
#     updates = {k: v for k, v in asdict(updates_data).items() if v is not None}
#     try:
#         updated = await service.update_profile_info(profile_id,updates)
#     except ValueError as e:
#         raise HTTPException(400, str(e))
#     return updated

@app.get("/client/contracts")
async def get_contracts_by_client(client_id:int,db:Session=Depends(get_db)):
    repo=SQLAlchemyContractRepository(db)
    service=ContractService(repo)
    result=await service.get_contracts_by_client(client_id)
    return result

@app.get("/agent/contracts")
async def get_all_contracts(db:Session=Depends(get_db)):
    repo = SQLAlchemyContractRepository(db)
    service = ContractService(repo)
    result=await service.get_all_contracts()
    return result

@app.get("/agent/contracts/contract")
async def get_contract(contract_id:int,db:Session=Depends(get_db)):
    repo = SQLAlchemyContractRepository(db)
    service = ContractService(repo)
    try:
        return await service.get_contract_by_id(contract_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))





