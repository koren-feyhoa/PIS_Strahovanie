from abc import ABC, abstractmethod
from typing import List

from domain.entities.ApplicationEntity import ApplicationEntity

class ApplicationRepository(ABC):
    @abstractmethod
    def add(self, application:ApplicationEntity)->ApplicationEntity:
        pass

    @abstractmethod
    def get_by_id(self, application_id:int)->ApplicationEntity:
        pass

    @abstractmethod
    def get_by_client_id(self, client_id:int)->List[ApplicationEntity]:
        pass

    @abstractmethod
    def get_all(self,skip: int = 0, limit: int = 0)->List[ApplicationEntity]:
        pass

    @abstractmethod
    def update(self, application_entity:ApplicationEntity)->ApplicationEntity:
        pass