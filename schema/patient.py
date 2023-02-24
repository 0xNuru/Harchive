from pydantic import BaseModel, EmailStr, SecretStr, root_validator
from pydantic import constr
from schema.user import User
from datetime import date
from models.patient import genderEnum
import re

password_regex = "(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}"


class Patient(BaseModel):
    name: constr(min_length=5)
    email: EmailStr
    password1: SecretStr
    password2: SecretStr
    gender: genderEnum
    dob: date
    phone: constr(min_length=11, max_length=14)
    address: constr(min_length=10)    
    insuranceID: str
    role : str = 'patient'

    class Config():
        orm_mode = True

   
    @root_validator()
    def verify_password_match(cls,values):
        password = values.get("password1").get_secret_value()
        confirm_password = values.get("password2").get_secret_value()
        if password != confirm_password:
            raise ValueError("The two passwords did not match.")
        if not re.match(password_regex, confirm_password):
            raise ValueError("Password length must atleast be 8 and contains alphabets ,number with a spectial character")
        return values