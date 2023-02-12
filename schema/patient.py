from User import User
from datetime import date


class Patient(User):
    dob: date
    gender: enumerate
    address: str
    insuranceID: str

    class Config():
        orm_mode = True
