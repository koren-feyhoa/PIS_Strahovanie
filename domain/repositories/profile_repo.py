from abc import ABC, abstractmethod
from typing import List

from domain.entities.ProfileEntity import ProfileEntity

class ProfileRepository(ABC):
    @abstractmethod
    def add(self,profile:ProfileEntity)->ProfileEntity:
        pass

    @abstractmethod
    def update(self,profile_entity:ProfileEntity)->ProfileEntity:
        pass

    @abstractmethod
    def get_by_client(self,client_id:int)->List[ProfileEntity]:
        pass

    @abstractmethod
    def get_by_id(self,profile_id:int)->ProfileEntity:
        pass

