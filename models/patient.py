#!/usr/bin/python3
"""
patient module

"""
import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum, null
from models.user import Users
from models.record import Record, Medication, Allergy,Immunization, Transactions
from sqlalchemy.orm import relationship
import sys
sys.path.insert(0, '..')


class genderEnum(enum.Enum):
    M = "M"
    F = "F"


class Patient(Users):
    """
        patient details
    """
    __tablename__ = "patient"
    id = Column(String, ForeignKey(
        'user.id',  ondelete="CASCADE"), primary_key=True)
    nin = Column(String(11), nullable=False, unique=True)
    insuranceID = Column(String(128), nullable=True, unique=False)
    address = Column(String(128), nullable=True)
    gender = Column(Enum(genderEnum, name="gender_enum"))
    role = Column(String(50), nullable=False, default='patient')
    patient_record = relationship(Record, cascade_backrefs='patient')
    patient_medication = relationship(Medication, cascade_backrefs='patient')
    patient_allergy = relationship(Allergy, cascade_backrefs='patient')
    patient_immunization = relationship(Immunization, cascade_backrefs='patient')
    patient_transaction = relationship(Transactions, cascade_backrefs='patient')
    
