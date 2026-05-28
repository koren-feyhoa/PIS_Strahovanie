from typing import List

from domain.entities.ApplicationEntity import ApplicationEntity
from domain.repositories.appication_repo import ApplicationRepository

class ApplicationServise:
    def __init__(self,application_repo:ApplicationRepository):
        self.repo=application_repo
    async def create_application(self,client_id: int, agent_id: int, insurance_type: str,
            profile_id: int)->ApplicationEntity:
        application_entity=ApplicationEntity.create(
            client_id=client_id,
            agent_id=agent_id,
            insurance_type=insurance_type,
            profile_id=profile_id,
            status_application="Заявка в обработке"
        )
        saved_application=self.repo.add(application_entity)
        return saved_application
    async def get_application_by_id(self,application_id:int)->ApplicationEntity:
        return self.repo.get_by_id(application_id)
    async def get_applications_by_client(self,client_id:int)->List[ApplicationEntity]:
        applicationsList= self.repo.get_by_client_id(client_id)
        return applicationsList
    async def get_all_applications(self)->List[ApplicationEntity]:
        return self.repo.get_all()
    async def update_price_application(self, application_id:int, updates: dict)->ApplicationEntity:
        application=self.repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")
        for key, value in updates.items():
            if hasattr(application,key) and value is not None:
                setattr(application,key,value)
        application.status_application="Заявка рассмотрена"
        return self.repo.update(application)
    async def update_status_reject(self,application_id:int)->ApplicationEntity:
        application=self.repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")
        application.status_application="Договор отклонён"
        return self.repo.update(application)

    async def update_status_accept(self,application_id:int)->ApplicationEntity:
        application=self.repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")
        application.status_application="Создание договора"
        return self.repo.update(application)


