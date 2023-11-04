#!/usr/bin/python3


import sys
sys.path.insert(0, '..')
from pydantic import BaseModel, EmailStr, SecretStr, root_validator, constr
from datetime import date
from models.patient import genderEnum
import re

from models.record import allergyEnum

password_regex = "(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}"


class Patient(BaseModel):
    name: constr(min_length=5)
    nin: constr(min_length=11, max_length=11)
    email: EmailStr
    password1: SecretStr
    password2: SecretStr
    gender: genderEnum
    dob: date
    phone: constr(min_length=11, max_length=14)
    address: constr(min_length=10)
    insuranceID: str

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


class ShowPatient(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True

class ShowPatientReg(BaseModel):
    name: str
    email: str
    message: str

    class Config():
        orm_mode = True


class PatientRecord(BaseModel):
    type: str
    DOB: date
    BloodType: constr(max_length=5)
    Height: float
    weight: float
    BMI: float

    class Config():
        orm_mode = True


class Medication(BaseModel):
    medication_name: str
    dosage: str
    start_date: date
    due_date: date
    reason: str

    class Config():
        orm_mode = True


class ShowMedication(BaseModel):
    medication_name: str
    dosage: str
    start_date: date
    due_date: date
    reason: str
    doctor_name: str

    class Config():
        orm_mode = True


class Allergy(BaseModel):
    allergy_name: str
    type: allergyEnum
    reactions: str
    more_info: str

    class Config():
        orm_mode = True


class ShowAllergy(BaseModel):
    allergy_name: str
    type: allergyEnum
    reactions: str
    more_info: str
    doctor_name: str

    class Config():
        orm_mode = True


class Immunization(BaseModel):
    name: str
    immunization_date: date
    immunization_location: str
    lot_number: str
    expiry_date: date
    more_info: str
    doctor_name: str

    class Config():
        orm_mode = True


class ShowImmunization(BaseModel):
    name: str
    immunization_date: date
    immunization_location: str
    lot_number: str
    expiry_date: date
    more_info: str
    doctor_name: str

    class Config():
        orm_mode = True


class Transaction(BaseModel):
    description: str
    quantity: float

    class Config():
        orm_mode = True
