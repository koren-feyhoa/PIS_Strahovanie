from JSON_function import DeserializaJSON, SerializeJSON
from domain.entities.ProfileEntity import ProfileEntity
from models import Profile as ProfileORM

def profile_orm_to_entity(orm:ProfileORM)->ProfileEntity:
    return ProfileEntity(
        client_id=orm.client_id,
        type_document=orm.type_document,
        info=DeserializaJSON(orm.info)
    )
def profile_entity_to_orm(ent:ProfileEntity)-> ProfileORM:
    return ProfileORM(
        client_id=ent.client_id,
        type_document=ent.type_document,
        info=SerializeJSON(ent.info)
    )