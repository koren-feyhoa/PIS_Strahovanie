from abc import ABC, abstractmethod
from domain.entities.ClientEntity import ClientEntity

class ClientRepository(ABC):
    @abstractmethod
    def add(self,client:ClientEntity)->ClientEntity:
        pass