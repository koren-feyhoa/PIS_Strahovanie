from domain.entities.ClientEntity import ClientEntity
from domain.repositories.client_repo import ClientRepository


class ClientService:
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

    async def update_client(self, client_id: int, updates: dict) -> ClientEntity:
        client = self.repo.get_by_id(client_id)
        if not client:
            raise ValueError("Client not found")
        for key, value in updates.items():
            if hasattr(client, key) and value is not None:
                setattr(client, key, value)
        return self.repo.update(client)