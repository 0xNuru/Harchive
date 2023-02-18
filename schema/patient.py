from pydantic import BaseModel


class Patient(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    password: str


# from schema.user import User
# from datetime import date


# class Patient(User):
#     dob: date
#     gender: enumerate
#     address: str
#     insuranceID: str

#     class Config():
#         orm_mode = True
