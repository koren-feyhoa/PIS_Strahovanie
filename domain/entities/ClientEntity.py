# domain/entities.py
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Any, Dict

import phonenumbers


# ------ Client ------
@dataclass
class ClientEntity:
    id[Optional]: int
    fullname: str
    phone: str
    email: str
    password: str  # храним хеш, а не пароль открытым текстом

    def __post_init__(self):
        if not self.fullname:
            raise ValueError("ФИО не может быть пустым")
        if '@' not in self.email:
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

