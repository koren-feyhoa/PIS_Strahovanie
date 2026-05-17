from sqlalchemy.orm import Session

from mappers.ProfileMapper import profile_entity_to_orm
from .profile_repo  import ProfileRepository
from domain.entities.ProfileEntity import ProfileEntity
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