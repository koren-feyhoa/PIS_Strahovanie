# services/contract_service.py
from datetime import date, datetime
from typing import List

from domain.entities.ContractEntity import ContractEntity
from domain.repositories.appication_repo import ApplicationRepository
from domain.repositories.contract_repo import ContractRepository
from storage import FileStorage

class ContractService:
    def __init__(self, contract_repo: ContractRepository):
        self.repo = contract_repo

    async def get_contract_by_id(self, contract_id: int) -> ContractEntity:
        contract= self.repo.get_by_id(contract_id)
        if contract is None:
            raise ValueError(f"no contract with id: {contract_id}")
        return contract
    async def get_contracts_by_client(self, client_id: int) -> List[ContractEntity]:
        return self.repo.get_by_client_id(client_id)
    async def get_all_contracts(self)->List[ContractEntity]:
        return self.repo.get_all()
