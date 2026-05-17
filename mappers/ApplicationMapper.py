from domain.entities.ApplicationEntity import ApplicationEntity
from models import Application as ApplicationORM

def application_orm_to_entity(orm:ApplicationORM)->ApplicationEntity:
    return ApplicationEntity(
        client_id=orm.client_id,
        agent_id=orm.agent_id,
        insurance_type=orm.insurance_type,
        data_create=orm.data_create,
        profile_id=orm.profile_id,
        status_application=orm.status_application,
        calculate_price=orm.calculate_price
    )

def application_entity_to_orm(entity:ApplicationEntity)->ApplicationORM:
    return ApplicationORM(
        client_id=entity.client_id,
        agent_id=entity.agent_id,
        insurance_type=entity.insurance_type,
        data_create=entity.data_create,
        profile_id=entity.profile_id,
        status_application=entity.status_application,
        calculate_price = entity.calculate_price
    )