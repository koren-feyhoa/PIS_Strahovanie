from abc import ABC, abstractmethod
from domain.entities.ApplicationEntity import ApplicationEntity

class ApplicationRepository(ABC):
    @abstractmethod
    def add(self, application:ApplicationEntity)->ApplicationEntity:
        pass