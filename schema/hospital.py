from pydantic import BaseModel
from typing import List
from patient import Patient
from healthWorker import HealthWorker
from insuranceCompany import InsuranceCompany


class Hospital(BaseModel):
    name: str
    address: str
    hospitalID: str
    patients: List[Patient] = []
    healthWorkers: List[HealthWorker] = []
    insuranceCompanines: List[InsuranceCompany] = []

    class Config():
        orm_mode = True
