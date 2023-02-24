from pydantic import BaseModel
from typing import List
from schema.patient import Patient
from schema.healthWorker import HealthWorker
from schema.insurance import Insurance


class Hospital(BaseModel):
    name: str
    address: str
    hospitalID: str
    phone: str

    class Config():
        orm_mode = True
