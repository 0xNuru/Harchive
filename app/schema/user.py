#!/usr/bin/python3


import re
from typing import Optional
from pydantic import BaseModel, EmailStr, SecretStr, root_validator, constr
import sys
sys.path.insert(0, '..')

password_regex = "(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}"


class User(BaseModel):
    name: constr(min_length=5)
    email: EmailStr
    phone: constr(min_length=11, max_length=14)
    address: constr(min_length=10)
    password1: SecretStr
    password2: SecretStr

    @root_validator()
    def verify_password_match(cls, values):
        password = values.get("password1").get_secret_value()
        confirm_password = values.get("password2").get_secret_value()
        if password != confirm_password:
            raise ValueError("The two passwords did not match.")
        if not re.match(password_regex, confirm_password):
            raise ValueError(
                "Password length must atleast be 8 and contain alphabets, number and atleast a spectial character")
        return values


class ShowUser(BaseModel):

    name: str
    email: str
    role: str 

    class Config():
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: SecretStr

class forgotPassword(BaseModel):
    email: EmailStr

class resetPassword(BaseModel):
    rPassword1: SecretStr
    rPassword2: SecretStr

    @root_validator()
    def verify_password_match(cls, values):
        password = values.get("rPassword1").get_secret_value()
        confirm_password = values.get("rPassword2").get_secret_value()
        if password != confirm_password:
            raise ValueError("The two passwords did not match.")
        if not re.match(password_regex, confirm_password):
            raise ValueError(
                "Password length must atleast be 8 and contain alphabets, number and atleast a spectial character")
        return values
