from domain.entities.AgentEntity import AgentEntity
from models import Agent as AgentORM

def agent_orm_to_entity(orm:AgentORM)->AgentEntity:
    return AgentEntity(
        fullname=orm.fullname,
        email=orm.email,
        password=orm.password
    )

def agent_entity_to_orm(entity:AgentEntity)->AgentORM:
    return AgentORM(
        fullname=entity.fullname,
        email=entity.email,
        password=entity.password
    )