from database import SessionLocal
from CURD import createClient

db = SessionLocal()
user = createClient(db, name="test", phone="123", email="test@test.com", password="123")
db.commit()
print(user)
db.close()