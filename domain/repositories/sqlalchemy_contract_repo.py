# repositories/sqlalchemy_contract_repo.py
from typing import List

from sqlalchemy.orm import Session
from .contract_repo  import ContractRepository
from domain.entities.ContractEntity import ContractEntity
from mappers.ContractMapper import contract_entity_to_orm, contract_orm_to_entity
from models import Contract as ContractORM

class SQLAlchemyContractRepository(ContractRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, contract: ContractEntity) -> ContractEntity:
        db_contract = contract_entity_to_orm(contract)
        self.db.add(db_contract)
        self.db.commit()
        self.db.refresh(db_contract)
        contract.id = db_contract.id
        return contract

    def get_by_id(self, contract_id:int) ->ContractEntity:
        orm=self.db.query(ContractORM).filter(ContractORM.id==contract_id).first()
        return contract_orm_to_entity(orm) if orm else None

    def get_by_client_id(self, client_id: int,skip: int = 0, limit: int = 100) -> List[ContractEntity]:
        orm = self.db.query(ContractORM).filter(ContractORM.client_id == client_id).offset(skip).limit(
            limit).all()
        return [contract_orm_to_entity(contract) for contract in orm]

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ContractEntity]:
        orm = self.db.query(ContractORM).offset(skip).limit(limit).all()
        return [contract_orm_to_entity(contract) for contract in orm]
