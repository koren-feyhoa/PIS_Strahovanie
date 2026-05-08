import json
from datetime import datetime
from xmlrpc.client import DateTime
import FileWork
from psycopg2 import Date
from sqlalchemy.orm import Session


from models import Client, Application, Profile, Contract
import pathlib

def createClient(db:Session,name:str,phone:str,email:str,password:str):
    newClient=Client(fullname=name,phone=phone,email=email,password=password)
    db.add(newClient)
    db.commit()
    db.refresh(newClient)
    return  newClient

def createApplication(db:Session, client_id:int, agent_id:int,insurance_type:str, data_create:DateTime,  profile_id:int, status_application:str,calculate_price:float ):
    newApplication=Application(client_id=client_id,agent_id=agent_id,insurance_type=insurance_type,data_create=data_create,profile_id=profile_id,status_application=status_application,calculate_price=calculate_price)
    db.add(newApplication)
    db.commit()
    db.refresh(newApplication)
    return  newApplication

def createProfile(db:Session, client_id:int, type_document:str,info:json):
    newProfile=Profile(client_id=client_id,type_document=type_document,info=info)
    db.add(newProfile)
    db.commit()
    db.refresh(newProfile)
    return newProfile

def getAllUserApplication(db:Session, client_id:int):
    applicationsAll=db.query(Application).filter(Application.client_id==client_id).all()
    return applicationsAll


def updateStatusApplication(db:Session,application_id:int,status:str):
    application=db.query(Application).filter(Application.id==application_id).first()
    if (application!=None):
        application.status_application=status
        db.commit()
def getUserApplication(db:Session,client_id:int):
    applicationsUser=db.query(Application).filter(Application.id==client_id).all()
    return applicationsUser

def updateClientName(db:Session,client_id:int, newName:str):
    client=db.query(Client).filter(Client.id==client_id).first()
    if (client!=None):
        client.fullname=newName
        db.commit()
def updateClientEmail(db:Session,client_id:int, newEmail:str):
    client=db.query(Client).filter(Client.id==client_id).first()
    if (client!=None):
        client.email=newEmail
        db.commit()
def updateProfile(db:Session,profile_id:int,newInfo:json):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if (profile!=None):
        profile.info==newInfo
        db.commit()

def deleteProfile(db:Session,profile_id:int):
    profile=db.query(Profile).filter(Profile.id==profile_id).first()
    db.delete(profile)
    db.commit()

def createContract(
    db: Session,
    application: Application,
    contract_number: int,
    date_start,  # используйте datetime.date или datetime.datetime
    date_end,
    file_path: pathlib.Path
) -> Contract:
    """Создаёт контракт и сохраняет информацию о файле."""
    contract = Contract(
        client_id=application.client_id,
        application_id=application.id,
        agent_id=application.agent_id,
        contract_number=contract_number,
        date_start=date_start,
        date_end=date_end,
        file_path=file_path.parent.as_posix(),   # папка (например "files/123")
        file_name=file_path.name,                # имя файла (например "c8e9...pdf")
        file_time=datetime.now()
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract

def getAllContracts(db:Session,agent_id:int):
    allContracts=db.query(Contract).filter(Contract.agent_id==agent_id).list()
    return allContracts

def getContractsByClient(db:Session, client_id:int):
    contracts=db.query(Contract).filter(Contract.client_id==client_id).list()
    return contracts

def getContractById(db:Session,contract_id:int):
    contract=db.query(Contract).filter(Contract.id==contract_id).fitst()
    return contract














