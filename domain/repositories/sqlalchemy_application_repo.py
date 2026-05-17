from domain.entities.ApplicationEntity import ApplicationEntity
from domain.repositories.appication_repo import ApplicationRepository
from sqlalchemy.orm import Session

from mappers.ApplicationMapper import application_entity_to_orm


class SQLAlchemyApplicationRepository(ApplicationRepository):
    def __init__(self,db:Session):
        self.db=db
    def add(self,application:ApplicationEntity)->ApplicationEntity:
        db_application=application_entity_to_orm(application)
        self.db.add(db_application)
        self.db.commit()
        self.db.refresh(db_application)
        application.id=db_application.id
        return application