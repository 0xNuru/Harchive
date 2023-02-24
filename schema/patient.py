from pydantic import BaseModel
from schema.user import User
from datetime import date
from models.patient import genderEnum


# class GenderEnum(str, Enum):
#     MALE = 'male'
#     FEMALE = 'female'


class Patient(BaseModel):
    dob: date
    gender: genderEnum
    address: str
    password: str
    name: str
    phone: str
    email : str
    insuranceID: str

    class Config():
        orm_mode = True
