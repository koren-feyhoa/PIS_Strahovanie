from sqlalchemy import Column, Integer, String, ForeignKey,JSON, DateTime, Float, Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from database import Base


class Client(Base):
    __tablename__='client'
    id=Column(Integer,primary_key=True)
    fullname = Column(String)
    phone:[str]=Column(String(30))
    email=Column(String(50), unique=True)
    password=Column(String)

    def __repr__(self) -> str:
        return f"Client(id={self.id}, fullname={self.fullname}, email={self.email})"

class Agent(Base):
    __tablename__ = 'agent'
    id = Column(Integer, primary_key=True)
    fullname = Column(String)
    email = Column(String(50), unique=True)

class Profile(Base):
    __tablename__ = 'profile'
    id:Mapped[int] = mapped_column(primary_key=True)
    client_id:Mapped[int] = mapped_column(ForeignKey('client.id'))
    type_document=Column(String)
    info=Column(JSON)

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
    def __repr__(self) -> str:
        return f"Application(id={self.id},status_application={self.status_application})"



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