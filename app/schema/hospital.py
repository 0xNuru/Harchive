#!/usr/bin/python3

import sys
sys.path.insert(0, '..')

from schema.user import User
from datetime import date
import re
from pydantic import BaseModel, EmailStr, SecretStr, constr, root_validator

from models.patient import genderEnum


password_regex = "(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}"


class HospitalAdmin(BaseModel):
    name: constr(min_length=5)
    email: EmailStr
    phone: constr(min_length=11, max_length=14)
    password1: SecretStr
    password2: SecretStr
    hospitalID: str

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


class Hospital(BaseModel):
    name: constr(min_length=5)
    address: constr(min_length=10)
    phone: constr(min_length=11, max_length=14)
    hospitalID: str

    class Config():
        orm_mode = True


class ShowHospital(BaseModel):

    name: str
    hospitalID: str

    class Config():
        orm_mode = True

class ShowHospitalReg(BaseModel):

    name: str
    hospitalID: str
    role: str   
    message: str

    class Config():
        orm_mode = True


class Doctor(BaseModel):
    name: constr(min_length=5)
    email: EmailStr
    password1: SecretStr
    password2: SecretStr
    gender: genderEnum
    dob: date
    phone: constr(min_length=11, max_length=14)
    speciality: str
    hospitalID: str

    class Config():
        orm_mode = True

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


class ShowDoctor(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True

class ShowDoctorReg(BaseModel):
    name: str
    email: str
    role: str
    message: str

    class Config():
        orm_mode = True


class HealthWorker(User):
    hospitalID: str

    class Config():
        orm_mode = True


class CheckIn(BaseModel):
    nin: constr(min_length=11, max_length=11)

    class Config():
        orm_mode = True
