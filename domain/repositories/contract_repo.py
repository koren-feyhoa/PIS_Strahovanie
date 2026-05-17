from abc import ABC, abstractmethod
from domain.entities.ContractEntity import ContractEntity

class ContractRepository(ABC):
    @abstractmethod
    def add(self, contract: ContractEntity) -> ContractEntity:
        pass

