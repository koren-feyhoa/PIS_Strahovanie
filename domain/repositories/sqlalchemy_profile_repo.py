from typing import List

from sqlalchemy.orm import Session

from mappers.ProfileMapper import profile_entity_to_orm, profile_orm_to_entity
from .profile_repo  import ProfileRepository
from domain.entities.ProfileEntity import ProfileEntity
from models import Profile as ProfileORM
class SQLAlchemyProfileRepository(ProfileRepository):
    def __init__(self, db: Session):
        self.db = db
    def add(self,profile:ProfileEntity)->ProfileEntity:
        db_profile=profile_entity_to_orm(profile)
        self.db.add(db_profile)
        self.db.commit()
        self.db.refresh(db_profile)
        profile.id=db_profile.id
        return profile

    def get_by_client(self,client_id:int) ->List[ProfileEntity]:
        orm=self.db.query(ProfileORM).filter(ProfileORM.client_id==client_id).all()
        return [profile_orm_to_entity(profile) for profile in orm]


    def get_by_id(self,profile_id:int) ->ProfileEntity:
        orm=self.db.query(ProfileORM).filter(ProfileORM.id==profile_id).first()
        return profile_orm_to_entity(orm)

    def update(self,profile_entity:ProfileEntity) ->ProfileEntity:
        orm=self.get_by_id(profile_entity.id)
        orm.info=profile_entity.info
        self.db.commit()
        self.db.refresh(orm)
        return profile_orm_to_entity(orm)

