from domain.entities.ClientEntity import ClientEntity
from domain.repositories.client_repo import ClientRepository


class ClientServise:
    def __init__(self,client_repo:ClientRepository):
        self.repo=client_repo

    async def create_client(self,fullname:str,phone:str,email:str,password:str)->ClientEntity:
        client_entity=ClientEntity.create(
            fullname=fullname,
            phone=phone,
            email=email,
            password=password
        )
        saved_client=self.repo.add(client_entity)
        return saved_client