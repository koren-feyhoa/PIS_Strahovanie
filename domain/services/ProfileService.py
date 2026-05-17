from typing import Dict, Any

from domain.entities.ProfileEntity import ProfileEntity
from domain.repositories.profile_repo import ProfileRepository


class ProfileService:
    def __init__(self,profile_repo:ProfileRepository):
        self.repo=profile_repo
    async def create_profile(self,client_id:int,type_document:str,info:Dict[str,Any])->ProfileEntity:
        profile_entity=ProfileEntity.create(
            client_id=client_id,
            type_document=type_document,
            info=info
        )
        saved_profile=self.repo.add(profile_entity)
        return saved_profile
