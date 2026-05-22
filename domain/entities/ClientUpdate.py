from dataclasses import dataclass
from typing import Optional

@dataclass
class ClientUpdate:
    fullname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None