#!/usr/bin/python3
"""
hospitalWorker module
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum
from models.person import Person
from sqlalchemy.orm import relationship
import sys
sys.path.insert(0, '..')


class HospitalWorker(Person):
    """
        hospitalWorker details
    """
    __tablename__ = "hospitalWorkers"
    id = Column(Integer, ForeignKey("person.id"), nullable=False)
    hospitalID = Column(String, ForeignKey("hospitals.id"), nullable=False)

    person = relationship("Person", back_populates="hospitalWorkers")
    hospitals = relationship("Hospital", back_populates="hospitalWorkers")
