from domain.entities.ClientEntity import ClientEntity
from domain.repositories.client_repo import ClientRepository
from sqlalchemy.orm import Session
from mappers.ClientMapper import client_entity_to_orm

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