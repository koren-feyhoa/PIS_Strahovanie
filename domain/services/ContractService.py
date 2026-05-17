# services/contract_service.py
from datetime import date, datetime

from domain.entities.ContractEntity import ContractEntity
from domain.repositories.contract_repo import ContractRepository
from storage import FileStorage

class ContractService:
    def __init__(self, contract_repo: ContractRepository):
        self.repo = contract_repo

    async def create_contract(
        self,
        client_id: int,
        application_id: int,
        agent_id: int,
        contract_number: str,
        start_date: date,
        end_date: date,
        file_upload,
    ) -> ContractEntity:
        # 1. Сохраняем файл (это внешний сервис, его тоже можно заменить моком)
        folder_path, file_name = await FileStorage.save(file_upload, client_id)
        file_time = datetime.now()

        # 2. Создаём доменную сущность (валидация внутри)
        contract_entity = ContractEntity.create(
            client_id=client_id,
            application_id=application_id,
            agent_id=agent_id,
            contract_number=contract_number,
            start_date=start_date,
            end_date=end_date,
            file_name=file_name,
            file_path=folder_path,
            file_time=file_time,
            status="Посмотреть"
        )

        # 3. Сохраняем через репозиторий
        saved_contract = self.repo.add(contract_entity)
        return saved_contract