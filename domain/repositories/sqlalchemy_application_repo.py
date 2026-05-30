from typing import List

from domain.entities.ApplicationEntity import ApplicationEntity
from domain.repositories.appication_repo import ApplicationRepository
from sqlalchemy.orm import Session
from models import Application as ApplicationORM
from mappers.ApplicationMapper import application_entity_to_orm, application_orm_to_entity


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
    def get_by_id(self, application_id:int) ->ApplicationEntity|None:
        orm=self.db.query(ApplicationORM).filter(ApplicationORM.id==application_id).first()
        if not orm:
            return None
        application_entity=application_orm_to_entity(orm)
        return application_entity
    def get_by_client_id(self, client_id:int,skip: int = 0, limit: int = 100) ->List[ApplicationEntity]:
        orm=self.db.query(ApplicationORM).filter(ApplicationORM.client_id==client_id).offset(skip).limit(limit).all()
        return [application_orm_to_entity(application) for application in orm]

    def get_all(self,skip: int = 0, limit: int = 100) ->List[ApplicationEntity]:
        orm=self.db.query(ApplicationORM).offset(skip).limit(limit).all()
        return [application_orm_to_entity(application) for application in orm]

    def update(self, application_entity:ApplicationEntity) ->ApplicationEntity:
        orm = self.db.query(ApplicationORM).filter(ApplicationORM.id==application_entity.id).first()
        if not orm:
            raise ValueError(f"Application with id {application_entity.id} not found")
        orm.calculate_price=application_entity.calculate_price
        orm.status_application=application_entity.status_application
        self.db.commit()
        self.db.refresh(orm)
        return application_orm_to_entity(orm)

