# repositories/sqlalchemy_contract_repo.py
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
        orm=self.db.query(ContractORM)
        return contract_orm_to_entity(orm)