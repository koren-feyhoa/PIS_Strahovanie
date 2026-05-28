from typing import List

from domain.entities.AgentEntity import AgentEntity
from domain.entities.ClientEntity import ClientEntity
from domain.repositories.agent_repo import AgentRepository
from domain.repositories.client_repo import ClientRepository
from mappers.AgentMapper import agent_orm_to_entity


class AgentServise:
    def __init__(self, client_repo:ClientRepository, agent_repo:AgentRepository):
        self.repo=agent_repo
        self.client_repo = client_repo
    def get_all_clients(self)->List[ClientEntity]:
        return self.client_repo.get_all()
    def get_by_id(self,agent_id:int)->AgentEntity:
        orm=self.client_repo.get_by_id(agent_id)
        return agent_orm_to_entity(orm)
