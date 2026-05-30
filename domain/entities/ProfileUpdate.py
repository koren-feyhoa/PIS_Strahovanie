from dataclasses import dataclass
from typing import Optional
from sqlalchemy import JSON

@dataclass
class ProfileUpdate:
    info:Optional[JSON]=None