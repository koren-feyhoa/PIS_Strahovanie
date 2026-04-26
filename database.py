from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

DATABASE_URL="postgresql://postgres:1111@localhost/BD_Strahovanie"
#DATABASE_URL = "postgresql://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Client(Base):
    __tablename__='client'
    id=Column(Integer,primary_key=True)
    fullname = Column(String)
    phone:[str]=Column(String(30))
    email=Column(String(50), unique=True)

class Profile(Base):
    __tablename__ = 'client'
    id:Mapped[int] = mapped_column(primary_key=True)
    client_id:Mapped[int] = mapped_column(ForeignKey('Client.id'))
    insurance_type:Mapped[str] = mapped_column(String(30))
