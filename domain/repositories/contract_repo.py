from abc import ABC, abstractmethod
from typing import List
from domain.entities.ContractEntity import ContractEntity

class ContractRepository(ABC):
    @abstractmethod
    def add(self, contract: ContractEntity) -> ContractEntity:
        pass

    @abstractmethod
    def get_by_id(self, contract_id:int)->ContractEntity:
        pass

    @abstractmethod
    def get_by_client_id(self, client_id: int) -> List[ContractEntity]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 0) -> List[ContractEntity]:
        pass


