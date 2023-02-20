#!/usr/bin/python3
"""
patient module
"""
import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum
from models.user import Users
from sqlalchemy.orm import relationship
import sys
sys.path.insert(0, '..')

class genderEnum(enum.Enum):
    M = 1
    F = 2


class Patient(Users):
    """
        patient details
    """
    __tablename__ = "patient"
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    dob = Column(Date, nullable=False)
    gender = Column(Enum(genderEnum), nullable=False)
    address = Column(String, nullable=False)
    insuranceID = Column(String, nullable=False)

    patient_record = relationship("record", backref="patient", lazy=True)
    __mapper_args__ = {
        'polymorphic_identity': 'patient'
    }
