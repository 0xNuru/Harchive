#!/usr/bin/python3
"""
patient module
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum
from models.user import User
from sqlalchemy.orm import relationship
import sys
sys.path.insert(0, '..')


class Patient(User):
    """
        patient details
    """
    __tablename__ = "patients"
    dob = Column(Date, nullable=False)
    gender = Column(Enum, nullable=False)
    address = Column(String, nullable=False)
    # insuranceID = Column(String, nullable=False)

    # patient_record = relationship("records", back_populates="patients")
