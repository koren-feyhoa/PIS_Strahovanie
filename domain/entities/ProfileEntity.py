from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Any, Dict

@dataclass
class ProfileEntity:
    id[Optional]: int
    client_id: int
    type_document: str
    info: Dict[str, Any]  # JSON-поле

    def __post_init__(self):
        if not self.type_document:
            raise ValueError("Тип документа не указан")
        if self.type_document not in ['ОСАГО', 'Паспорт РФ', 'Водительские права', 'Машина', 'ВетПаспорт']:
            raise ValueError("Тип документа должен быть из списка: 'ОСАГО', 'Паспорт РФ', 'Водительские права', 'Машина', 'ВетПаспорт'")
        if not self.info:
            raise ValueError("Заполните все поля")

    @classmethod
    def create(cls, client_id: int, type_document: str, info: Dict[str, Any]) -> "ProfileEntity":
        return cls(client_id=client_id, type_document=type_document, info=info)

