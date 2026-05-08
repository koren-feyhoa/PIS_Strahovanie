from datetime import datetime,date

import pathlib
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import SessionLocal
import CURD
import models
from domain.entities.Contract import ContractEntity
from mappers import contract_entity_to_orm
from storage import FileStorage
from fastapi.responses import FileResponse
app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
print("!!! NEW VERSION OF main.py LOADED !!!")
import sys; print(sys.executable)  # добавить временно в main.py
@app.get("/test_route")
def test():
    return {"message": "ok"}
@app.post("/client/")
def createClient(name:str,phone:str,email:str,password:str, db: Session = Depends(get_db)):
    return CURD.createClient(db, name, phone, email, password)

@app.post("/client/newApplication")
def createApplication(client_id:int, agent_id:int,insurance_type:str, data_create:datetime,  profile_id:int, status_application:str,calculate_price:float , db:Session=Depends(get_db)):
    return CURD.createApplication(db,client_id,agent_id,insurance_type,data_create,profile_id,status_application,calculate_price)

@app.get("/client/myApplications")
def getAllUserApplication(id_client: int, db:Session=Depends(get_db)):
    return CURD.getAllUserApplication(db,id_client)

@app.post("/agent/contracts/rftgyhujio")
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
    # 1. Сохраняем файл (как раньше)
    folder_path, file_name = await FileStorage.save(file, client_id)
    file_time = datetime.now()

    # 2. Создаём доменную сущность (сработает валидация в __post_init__)
    contract_entity = ContractEntity.create(
        client_id=client_id,
        application_id=application_id,
        agent_id=agent_id,
        contract_number=contract_number,
        start_date=start_date,
        end_date=end_date,
        file_name=file_name,
        file_path=folder_path,
        file_time=file_time,
        status="Посмотреть"
    )

    # 3. Маппим entity → ORM и сохраняем в БД
    db_contract = contract_entity_to_orm(contract_entity)
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)

    # 4. Обновляем id в entity (для ответа)
    contract_entity.id = db_contract.id

    return contract_entity

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
    contracts=CURD.getContractsByClient(db,client_id).list()
    return contracts







