import json
from xmlrpc.client import DateTime

from sqlalchemy.orm import Session
from models import Client, Application, Profile


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








