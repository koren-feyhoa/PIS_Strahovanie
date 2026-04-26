from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String,ForeignKey, create_engine

class Base(DeclarativeBase):
	pass

class Client(Base):
    __tablename__='client'
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: [str] = mapped_column(String(50))
    phone:[str]=mapped_column(String(30))
    email:[str]=mapped_column(String(50))

class Profile(Base):
    __tablename__ = 'client'
    id:Mapped[int] = mapped_column(primary_key=True)
    client_id:Mapped[int] = mapped_column(ForeignKey('Client.id'))
    insurance_type:Mapped[str] = mapped_column(String(30))

