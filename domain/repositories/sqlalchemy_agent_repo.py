from typing import List

from domain.entities.ClientEntity import ClientEntity
from domain.repositories.agent_repo import AgentRepository
from sqlalchemy.orm import Session

from mappers.ClientMapper import client_orm_to_entity
from models import Client as ClientORM
from domain.entities.AgentEntity import AgentEntity

class SQLAlchemyAgentRepository(AgentRepository):
    def __init__(self,db:Session):
        self.db=db
    def get_all_clients(self, skip: int=0, limit: int=100)->List[ClientEntity]:
        clients=self.db.query(ClientORM).offset(skip).limit(limit).all()
        return  [client_orm_to_entity(client) for client in clients]