from pydantic import BaseModel
from typing import List
from schema.patient import Patient
from schema.healthWorker import HealthWorker
from schema.insurance import Insurance


class Hospital(BaseModel):
    name: str
    address: str
    hospitalID: str
    patients: List[Patient] = []
    healthWorkers: List[HealthWorker] = []
    insuranceCompanines: List[Insurance] = []

    class Config():
        orm_mode = True
