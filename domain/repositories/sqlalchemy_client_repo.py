from typing import List

from domain.entities.ClientEntity import ClientEntity
from domain.repositories.client_repo import ClientRepository
from sqlalchemy.orm import Session
from mappers.ClientMapper import client_entity_to_orm, client_orm_to_entity
from models import Client as ClientORM

class SQLAlchemyClientRepository(ClientRepository):
    def __init__(self,db:Session):
        self.db=db

    def add(self,client:ClientEntity)->ClientEntity:
        db_client=client_entity_to_orm(client)
        self.db.add(db_client)
        self.db.commit()
        self.db.refresh(db_client)
        client.id = db_client.id
        return client

    def get_by_id(self, client_id: int) -> ClientEntity|None:
        orm = self.db.query(ClientORM).filter(ClientORM.id == client_id).first()
        if not orm:
            return None
        return client_orm_to_entity(orm)

    def update(self,client:ClientEntity) ->ClientEntity:
        orm=self.db.query(ClientORM).filter(ClientORM.id==client.id).first()
        if not orm:
            raise ValueError(f"Client with id {client.id} not found")
        orm.fullname=client.fullname
        orm.email=client.email
        orm.phone=client.phone
        self.db.commit()
        self.db.refresh(orm)
        return client_orm_to_entity(orm)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ClientEntity]:
        clients = self.db.query(ClientORM).offset(skip).limit(limit).all()
        return [client_orm_to_entity(client) for client in clients]
