from dataclasses import dataclass
from typing import Optional

@dataclass
class ApplicationUpdate:
    calculate_price: Optional[float]=None