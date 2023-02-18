#!/usr/bin/python3
"""
hospitalWorker module
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum
from models.user import user
from sqlalchemy.orm import relationship
import sys
sys.path.insert(0, '..')


class HospitalWorker(user):
    """
        hospitalWorker details
    """
    __tablename__ = "hospitalWorkers"
    id = Column(Integer, ForeignKey("user.id"), nullable=False)
    hospitalID = Column(String, ForeignKey("hospitals.id"), nullable=False)

    user = relationship("user", back_populates="hospitalWorkers")
    hospitals = relationship("Hospital", back_populates="hospitalWorkers")
