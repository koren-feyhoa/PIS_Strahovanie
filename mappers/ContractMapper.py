# ContractMapper.py
from domain.entities.Contract import ContractEntity
from models import Contract as ContractORM  # ваша SQLAlchemy модель

def contract_orm_to_entity(orm: ContractORM) -> ContractEntity:
    return ContractEntity(
        client_id=orm.client_id,
        application_id=orm.application_id,
        agent_id=orm.agent_id,
        contract_number=orm.contractNumber,
        start_date=orm.start_date,
        end_date=orm.end_date,
        file_name=orm.file_name,
        file_path=orm.file_path,
        file_time=orm.file_time,
        status_contract=orm.status_contract
    )

def contract_entity_to_orm(entity: ContractEntity) -> ContractORM:
    return ContractORM(
        client_id=entity.client_id,
        application_id=entity.application_id,
        agent_id=entity.agent_id,
        contractNumber=entity.contract_number,
        start_date=entity.start_date,
        end_date=entity.end_date,
        file_name=entity.file_name,
        file_path=entity.file_path,
        file_time=entity.file_time,
        status_contract=entity.status_contract
    )