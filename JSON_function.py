import json
from typing import Dict


def SerializeJSON(Dictionary:Dict[str,str]):
    return json.dumps(Dictionary)

def DeserializaJSON(strJSON: str):
    return json.loads(strJSON)