# domain/entities.py
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Any, Dict

@dataclass
class ApplicationEntity:
    id[Optional]: int
    client_id: int
    agent_id: int
    insurance_type: str
    data_create: datetime
    profile_id: int
    status_application: str
    calculate_price: float=None

    def __post_init__(self):
        if not self.insurance_type:
            raise ValueError("Тип страхования обязателен")
        if self.insurance_type.strip() not in ['Клещ', 'Животное', 'Животное', 'ОСАГО', 'ВетПаспорт']:
            raise ValueError( "Тип документа должен быть из списка: 'ОСАГО', 'Паспорт РФ', 'Водительские права', 'Машина', 'ВетПаспорт'")
        if self.calculate_price is not None and self.calculate_price < 0:
            raise ValueError("Цена не может быть отрицательной")

    @classmethod
    def create(cls,client_id: int, agent_id: int, insurance_type: str,
               profile_id: int, status_application: str = "Заявка в обработке") -> "ApplicationEntity":
        return cls(
            client_id=client_id,
            agent_id=agent_id,
            insurance_type=insurance_type,
            data_create=datetime.now(),
            profile_id=profile_id,
            status_application=status_application,
        )