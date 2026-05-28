from abc import ABC, abstractmethod
from typing import List

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

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 0) -> List[ClientEntity]:
        pass