from pydantic import BaseModel
from typing import List
from patient import Patient
from hospital import Hospital


class InsuranceCompany(BaseModel):
    name: str
    address: str
    insuranceID: str
    patients: List[Patient] = []
    memberHospital: List[Hospital] = []

    class Config():
        orm_mode = True
