# services/contract_service.py
from datetime import date, datetime

from domain.entities.ContractEntity import ContractEntity
from domain.repositories.appication_repo import ApplicationRepository
from domain.repositories.contract_repo import ContractRepository
from storage import FileStorage

class ContractService:
    def __init__(self, contract_repo: ContractRepository, app_repo:ApplicationRepository):
        self.repo = contract_repo
        self.app_repo= app_repo


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
        application = self.app_repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")
        if application.status_application != "Создание договора":
            raise ValueError("Контракт можно создать только из заявки со статусом 'Создание договора'")
        folder_path, file_name = await FileStorage.save(file_upload, client_id)
        file_time = datetime.now()

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
        application.status_application = "Договор заключён"
        self.app_repo.update(application)
        saved_contract = self.repo.add(contract_entity)
        return saved_contract
