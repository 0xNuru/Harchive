from datetime import date
import re
from pydantic import BaseModel, EmailStr, SecretStr, constr, root_validator
from typing import List
from models.patient import genderEnum
from schema.patient import Patient

password_regex = "(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}"


class InAdmin(BaseModel):
    name: constr(min_length=5)
    email: EmailStr
    phone: constr(min_length=11, max_length=14)
    password1: SecretStr
    password2: SecretStr
    insuranceID: str
    role: str = 'insurance_admin'

    @root_validator()
    def verify_password_match(cls, values):
        password = values.get("password2").get_secret_value()
        confirm_password = values.get("password2").get_secret_value()
        if password != confirm_password:
            raise ValueError("The two passwords did not match.")
        if not re.match(password_regex, confirm_password):
            raise ValueError(
                "Password length must atleast be 8 and contains alphabets ,number with a spectial character")
        return values


class Insurance(BaseModel):
    name: constr(min_length=5)
    address: constr(min_length=10)
    phone: constr(min_length=11, max_length=14)
    insuranceID: str

    class Config():
        orm_mode = True


class ShowInsurance(BaseModel):

    name: str
    insuranceID: str

    class Config():
        orm_mode = True
