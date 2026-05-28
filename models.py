import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
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
    password: Mapped[str]=mapped_column(String(50))
class Profile(Base):
    __tablename__ = 'profile'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_id:Mapped[int] = mapped_column(ForeignKey('client.id'))
    type_document=Column(String)
    info=Column(JSON)

class Application(Base):
    __tablename__='application'
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'))
    agent_id: Mapped[int] = mapped_column(ForeignKey('agent.id'))
    insurance_type: Mapped[str] = mapped_column(String(30))
    data_create: Mapped[DateTime] = mapped_column(DateTime)
    profile_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    status_application: Mapped[str] = mapped_column(String(20))
    calculate_price: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
def __repr__(self) -> str:
        return f"Application(id={self.id},status_application={self.status_application})"



class Contract(Base):
    __tablename__ = 'contract'
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'))
    application_id: Mapped[int] = mapped_column(ForeignKey('application.id'))
    agent_id: Mapped[int] = mapped_column(ForeignKey('agent.id'))
    contractNumber: Mapped[str] = mapped_column(String)
    start_date: Mapped[Date] = mapped_column(Date)
    end_date: Mapped[Date] = mapped_column(Date)
    file_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    file_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    file_time: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)
    status_contract: Mapped[str] = mapped_column(String)
