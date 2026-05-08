from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Any, Dict

@dataclass
class ProfileEntity:
    id: int
    client_id: int
    type_document: str
    info: Dict[str, Any]  # JSON-поле

    def __post_init__(self):
        if not self.type_document:
            raise ValueError("Тип документа не указан")
        if not isinstance(self.info, dict):
            raise ValueError("info должно быть словарём")

    @classmethod
    def create(cls,id:int, client_id: int, type_document: str, info: Dict[str, Any]) -> "ProfileEntity":
        return cls(id=id, client_id=client_id, type_document=type_document, info=info)

