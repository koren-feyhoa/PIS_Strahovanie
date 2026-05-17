from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Any, Dict
@dataclass
class ContractEntity:
    id[Optional]: int
    client_id: int
    application_id: int
    agent_id: int
    contract_number: str
    start_date: date
    end_date: date
    file_name: Optional[str]
    file_path: Optional[str]
    file_time: Optional[datetime]
    status_contract: str

    def __post_init__(self):
        if self.start_date >= self.end_date:
            raise ValueError("Дата начала должна быть раньше даты окончания")
        if not self.contract_number or not self.contract_number.strip():
            raise ValueError("Номер договора не может быть пустым")
        if not self.file_name or not self.file_path or not self.file_time:
            raise ValueError("Файл не загружен")


    @classmethod
    def create(cls,
               client_id: int,
               application_id: int,
               agent_id: int,
               contract_number: str,
               start_date: date,
               end_date: date,
               file_name: Optional[str] = None,
               file_path: Optional[str] = None,
               file_time: Optional[datetime] = None,
               status: str = "Посмотреть") -> "ContractEntity":
        return cls(
            client_id=client_id,
            application_id=application_id,
            agent_id=agent_id,
            contract_number=contract_number,
            start_date=start_date,
            end_date=end_date,
            file_name=file_name,
            file_path=file_path,
            file_time=file_time,
            status_contract=status
        )
