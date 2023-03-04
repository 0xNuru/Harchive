#!/usr/bin/python3
"""
patient module

"""
import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum, null
from models.user import Users
from models.record import Record
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
    insuranceID = Column(String(128), nullable=True, unique=True)
    address = Column(String(128), nullable=False)
    role = Column(String(50), nullable=False, default='patient')
    patient_record = relationship(Record, cascade_backrefs='patient')
