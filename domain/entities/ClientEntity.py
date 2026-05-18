# domain/entities.py
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Any, Dict
import re
import phonenumbers


# ------ Client ------
@dataclass
class ClientEntity:

    fullname: str
    phone: str
    email: str
    password: str
    id: Optional[int] = None

    def __post_init__(self):
        if not self.fullname:
            raise ValueError("ФИО не может быть пустым")
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(self.email):
            raise ValueError("Некорректный email")
        try:
            parsed = phonenumbers.parse(self.phone, None)  # None = определить страну автоматически
            if not phonenumbers.is_valid_number(parsed):
                raise ValueError("Введите корректный номер телефона")
        except phonenumbers.NumberParseException:
            raise ValueError("Неверный формат номера телефона")


    @classmethod
    def create(cls, fullname: str, phone: str, email: str, password: str) -> "ClientEntity":
        return cls(
            fullname=fullname,
            phone=phone,
            email=email,
            password=password
        )

