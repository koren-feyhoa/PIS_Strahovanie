from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import CURD

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def createClient(name:str,phone:str,email:str,password:str, db: Session = Depends(get_db)):
    return CURD.createClient(db, name, phone, email, password)

createClient("jhgvk","567890","cfghjk","56789ghj",Session = Depends(get_db))