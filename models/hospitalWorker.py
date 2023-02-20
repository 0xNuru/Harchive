#!/usr/bin/python3
"""
hospitalWorker module
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum
from models.user import user
from sqlalchemy.orm import relationship
import sys
sys.path.insert(0, '..')


class HospitalWorkers(BaseModel, Base):
    """
        hospitalWorker details
    """
    __tablename__ = "hospitalWorkers"
    id = Column(Integer, ForeignKey("user.id"), nullable=False)
    hospitalID = Column(String, ForeignKey("hospitals.id"), nullable=False)

    doctor = relationship("Doctor", back_populates="hospitalWorkers")
    hospital = relationship("Hospital", back_populates="hospitalWorkers")

class Doctor(user):
    """
        Doctor details
    """
    __tablename__ = "doctor"
    id = Column(Integer, ForeignKey("user.id"),primary_key=True, nullable=False)
    speciality = Column(String, nullable=False)
    hospitalID = Column(String, ForeignKey("hospitals.id"), nullable=False)
    hospitalworkers = relationship("hospitalworkers", back_populates="doctor")
    __mapper_args__ = {
        'polymorphic_identity': 'doctor'
    }

