from domain.entities.ClientEntity import ClientEntity
from models import Client as ClientORM

def client_orm_to_entity(orm:ClientORM)->ClientEntity:
    return ClientEntity(
        fullname=orm.fullname,
        phone=orm.phone,
        email=orm.email,
        password=orm.password
    )

def client_entity_to_orm(entity:ClientEntity)->ClientORM:
    return ClientORM(
        fullname=entity.fullname,
        phone=entity.phone,
        email=entity.email,
        password=entity.password
    )