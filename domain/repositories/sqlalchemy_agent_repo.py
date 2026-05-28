from typing import List

from domain.entities.ClientEntity import ClientEntity
from domain.repositories.agent_repo import AgentRepository
from sqlalchemy.orm import Session

from mappers.AgentMapper import agent_orm_to_entity
from mappers.ClientMapper import client_orm_to_entity
from models import Agent as AgentORM
from domain.entities.AgentEntity import AgentEntity

class SQLAlchemyAgentRepository(AgentRepository):
    def __init__(self,db:Session):
        self.db=db
    def get_by_id(self, agent_id:int) ->AgentEntity:
        agent=(self.db.query(AgentORM)
               .filter(AgentORM.id==AgentEntity.id)
               .first())
        if not agent:
            raise ValueError(f"Agent with id {agent.id} not found")
        return agent_orm_to_entity(agent)