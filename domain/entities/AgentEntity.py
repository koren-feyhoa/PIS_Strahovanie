from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Any, Dict
# ------ Agent ------
@dataclass
class AgentEntity:

    fullname: str
    email: str
    id: Optional[int] = None

    def __post_init__(self):
        if not self.fullname:
            raise ValueError("Имя агента не может быть пустым")
        if '@' not in self.email:
            raise ValueError("Некорректный email агента")

    @classmethod
    def create(cls, fullname: str, email: str) -> "AgentEntity":
        return cls(id=None, fullname=fullname, email=email)
