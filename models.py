import enum
import uuid
from datetime import datetime
from tkinter.constants import CASCADE
from typing import Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey,JSON, DateTime, Float, Date, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from database import Base

class RoleEnum(str, enum.Enum):
    CLIENT="клиент"
    AGENT="агент"

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

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[RoleEnum] = mapped_column(default=RoleEnum.CLIENT, nullable=False)
    name:Mapped[str]=mapped_column(nullable=True)
    last_name:Mapped[str]=mapped_column(nullable=True)
    email:Mapped[str]=mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(50))
    phone: Mapped [str] = mapped_column(String(30), nullable=True)



#?????????????????????????????

class Document(Base):
    __tablename__='document'
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id:Mapped[int] = mapped_column(ForeignKey('client.id', ondelete=CASCADE))
    document_type_id:Mapped[int]=mapped_column(ForeignKey('document_type.id',ondelete=CASCADE))
    created_at:Mapped[Date]=mapped_column(Date)
    updated_at:Mapped[Date]=mapped_column(Date)

class DocumentType(Base):
    __tablename__ = 'document_type'
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String)
    description:Mapped[str]=mapped_column(String)

class InsuranceType(Base):
    __tablename__ = 'insurance_type'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)


class RequiredDocuments(Base):
    __tablename__='required_document'
    insurance_type_id:Mapped[int]=mapped_column(ForeignKey('insurance_type.id', ondelete=CASCADE),primary_key=True,  nullable=False)
    document_type_id:Mapped[int]=mapped_column(ForeignKey('document_type.id', ondelete=CASCADE),primary_key=True,  nullable=False)
    __table_args__=(
        PrimaryKeyConstraint('insurance_type_id', 'document_type_id'),
    )

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

class Passport(Base):
    __tablename__='passport'
    id: Mapped[int]=mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey('document.id'))
    series:Mapped[int]=mapped_column(Integer)
    number: Mapped[int] = mapped_column(Integer)
    name:Mapped[str]=mapped_column(String)
    last_name:Mapped[str]=mapped_column(String)
    patronymic:Mapped[str]=mapped_column(String)
    day_of_birth:Mapped[Date]=mapped_column(Date)
    day_of_get:Mapped[Date]=mapped_column(Date)
    who_give:Mapped[str]=mapped_column(String)

#Доделать профайл переделать агента и клиента с выделением роли