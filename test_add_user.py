from CURD import getAllUserApplication, updateStatusApplication
from database import SessionLocal
import  CURD
from models import Client

db = SessionLocal()
#user = CURD.createClient(db, name="test", phone="123", email="test@test.com", password="123")
#db.commit()
#print(user)
#print(getAllUserApplication(db,1))
#db.commit()
#db.close()

print(updateStatusApplication(db,3,'Договор заключен'))
db.commit()
db.close()

