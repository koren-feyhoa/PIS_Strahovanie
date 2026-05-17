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


