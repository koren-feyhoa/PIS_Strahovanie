from abc import ABC, abstractmethod
from domain.entities.AgentEntity import AgentEntity
from domain.entities.ClientEntity import ClientEntity


class AgentRepository(ABC):
    @abstractmethod
    def get_by_id(self, agent_id:int)->AgentEntity:
        pass