from person import Person
from datetime import date


class Patient(Person):
    dob: date
    gender: enumerate
    address: str
    insuranceID: str

    class Config():
        orm_mode = True
