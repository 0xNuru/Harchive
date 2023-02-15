#!/usr/bin/python3
"""
Hospital module

"""
from models.base_model import BaseModel, Base

from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
import sys
sys.path.insert(0, '..')


class Hospital(BaseModel, Base):
    """
        hospital details
    """
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String(128), nullable=False)
    address = Column(String(128), nullable=False)
    hospitalID = Column(String(128), nullable=False)

    hospitalWorker = relationship("hospitalWorker", back_populates="hospitals")
