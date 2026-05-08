# domain/entities.py
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Any, Dict

@dataclass
class ApplicationEntity:
    id: int
    client_id: int
    agent_id: int
    insurance_type: str
    data_create: datetime
    profile_id: int
    status_application: str
    calculate_price: Optional[float]

    def __post_init__(self):
        if not self.insurance_type:
            raise ValueError("Тип страхования обязателен")
        if self.calculate_price is not None and self.calculate_price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if self.status_application not in ["Заявка в обработке", "Заявка рассмотрена", "Договор заключен", "Договор отклонен"]:
            raise ValueError(f"Недопустимый статус заявки: {self.status_application}")

    @classmethod
    def create(cls, id:int,client_id: int, agent_id: int, insurance_type: str,
               profile_id: int, status: str = "Заявка в обработке") -> "ApplicationEntity":
        return cls(
            id=id,
            client_id=client_id,
            agent_id=agent_id,
            insurance_type=insurance_type,
            data_create=datetime.now(),
            profile_id=profile_id,
            status_application=status,
            calculate_price=None
        )