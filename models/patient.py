#!/usr/bin/python3
"""
patient module
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum
from models.person import Person
from sqlalchemy.orm import relationship
import sys
sys.path.insert(0, '..')


class Patient(Person):
    """
        patient details
    """
    __tablename__ = "patients"
    id = Column(Integer, ForeignKey("person.id"), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(Enum, nullable=False)
    address = Column(String, nullable=False)
    insuranceID = Column(String, nullable=False)

    person = relationship("Person", back_populates="patients")
