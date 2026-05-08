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