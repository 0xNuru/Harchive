from pydantic import BaseModel
from typing import List
from schema.patient import Patient


class Insurance(BaseModel):
    name: str
    address: str
    phone: str
    insuranceID: str

    class Config():
        orm_mode = True
