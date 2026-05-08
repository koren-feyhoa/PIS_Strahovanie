# domain/entities.py
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Any, Dict

# ------ Client ------
@dataclass
class ClientEntity:
    id: int
    fullname: str
    phone: str
    email: str
    password: str  # храним хеш, а не пароль открытым текстом

    def __post_init__(self):
        if not self.fullname:
            raise ValueError("ФИО не может быть пустым")
        if '@' not in self.email:
            raise ValueError("Некорректный email")
        if len(self.phone) < 10:
            raise ValueError("Номер телефона слишком короткий")

    @classmethod
    def create(cls,id:int, fullname: str, phone: str, email: str, password: str) -> "ClientEntity":
        return cls(
            id=id,
            fullname=fullname,
            phone=phone,
            email=email,
            password=password
        )

