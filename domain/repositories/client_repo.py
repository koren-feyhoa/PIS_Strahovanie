from abc import ABC, abstractmethod
from domain.entities.ClientEntity import ClientEntity

class ClientRepository(ABC):
    @abstractmethod
    def add(self,client:ClientEntity)->ClientEntity:
        pass

    @abstractmethod
    def update(self,client:ClientEntity)->ClientEntity:
        pass
    @abstractmethod
    def get_by_id(self,client_id:int)->ClientEntity|None:
        pass
