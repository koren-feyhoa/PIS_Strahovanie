from xmlrpc.client import DateTime

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import CURD
import models

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/user/")
def createClient(name:str,phone:str,email:str,password:str, db: Session = Depends(get_db)):
    return CURD.createClient(db, name, phone, email, password)

@app.post("/user/newApplication")
def createApplication(client_id:int, agent_id:int,insurance_type:str, data_create:DateTime,  profile_id:int, status_application:str,calculate_price:float , db:Session=Depends(get_db)):
    return CURD.createApplication(db,client_id,agent_id,insurance_type,data_create,profile_id,status_application,calculate_price)

def getAllUserApplication(id_client: int, db:Session=Depends(get_db)):
    return CURD.getAllUserApplication(db,id_client)



