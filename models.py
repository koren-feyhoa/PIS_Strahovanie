from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
class Client(Base):
    __tablename__='client'
    id=Column(Integer,primary_key=True)
    fullname = Column(String)
    phone:[str]=Column(String(30))
    email=Column(String(50), unique=True)
    password=Column(String)

class Agent(Base):
    __tablename__ = 'agent'
    id = Column(Integer, primary_key=True)
    fullname = Column(String)
    email = Column(String(50), unique=True)

class Profile(Base):
    __tablename__ = 'profile'
    id:Mapped[int] = mapped_column(primary_key=True)
    client_id:Mapped[int] = mapped_column(ForeignKey('client.id'))
    insurance_type:Mapped[str] = mapped_column(String(30))

class Application(Base):
    __tablename__='application'
    id=Column(Integer,primary_key=True)
    client_id:Mapped[int] = mapped_column(ForeignKey('client.id'))
    agent_id=Column(ForeignKey('agent.id'))
    insurance_type: Mapped[str] = mapped_column(String(30))
    data_create=Column(DateTime)
    profile_id=Column(ForeignKey('profile.id'))
    status_application=Column(String())
    calculate_price=Column(Float())

class Contract(Base):
    __tablename__ = 'contract'
    id = Column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'))
    application_id=Column(Integer, ForeignKey('application.id'))
    agent_id = Column(ForeignKey('agent.id'))
    contractNumber=Column(String)
    start_date=Column(Date())
    end_date=Column(Date())
    file_name=Column(String())
    file_path=Column(String())