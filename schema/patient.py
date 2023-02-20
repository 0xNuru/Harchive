from pydantic import BaseModel
from schema.user import User
from datetime import date
from enum import Enum


class GenderEnum(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


class Patient(User):
    dob: date
    gender: Enum
    address: str
    # insuranceID: str

    class Config():
        orm_mode = True
