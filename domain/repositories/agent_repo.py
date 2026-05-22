from abc import ABC, abstractmethod
from domain.entities.AgentEntity import AgentEntity

class AgentRepository(ABC):
    @abstractmethod
    def get_all_clients(self, agent:AgentEntity)->AgentEntity:
        pass