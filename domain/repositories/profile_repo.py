from abc import ABC, abstractmethod
from domain.entities.ProfileEntity import ProfileEntity

class ProfileRepository(ABC):
    @abstractmethod
    def add(self,profile:ProfileEntity)->ProfileEntity:
        pass
