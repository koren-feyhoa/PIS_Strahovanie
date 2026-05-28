# domain/entities.py
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Any, Dict

@dataclass
class ApplicationEntity:

    client_id: int
    agent_id: int
    insurance_type: str
    data_create: datetime
    profile_id: int
    status_application: str
    calculate_price: float=None
    id: Optional[int] = None

    def validate(self):
        if not self.insurance_type:
            raise ValueError("Тип страхования обязателен")
        if self.insurance_type.strip() not in ['Клещ', 'Животное', 'Животное', 'ОСАГО']:
            raise ValueError( "Тип документа должен быть из списка: 'Клещ', 'Животное', 'Животное', 'ОСАГО'")
        if self.calculate_price is not None and self.calculate_price < 0:
            raise ValueError("Цена не может быть отрицательной")

    @classmethod
    def create(cls,client_id: int, agent_id: int, insurance_type: str,
               profile_id: int, status_application: str = "Заявка в обработке") -> "ApplicationEntity":
         application=cls(
            client_id=client_id,
            agent_id=agent_id,
            insurance_type=insurance_type,
            data_create=datetime.now(),
            profile_id=profile_id,
            status_application=status_application,
        )
         application.validate()
         return application