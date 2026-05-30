from typing import Dict, Any, List

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

    async def get_profiles_by_client_id(self,client_id:int)->List[ProfileEntity]|None:
        profiles=self.repo.get_by_client(client_id)
        if not profiles:
            return None
        return profiles

    async def get_profile_by_id(self,profile_id:int)->ProfileEntity:
        profile=self.repo.get_by_id(profile_id)
        if not profile:
            raise ValueError("Профиля не существует")
        return profile

    async def update_profile_info(self,profile_id:int,updates:dict)->ProfileEntity:
        profile=self.get_profile_by_id(profile_id)
        for key, value in updates.items():
            if hasattr(profile, key) and value is not None:
                setattr(profile, key, value)
        return self.repo.update(profile)

