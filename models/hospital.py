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
    name = Column(String(128), nullable=False)
    address = Column(String(128), nullable=False)
    hospitalID = Column(String(128), nullable=False)
    phone = Column(String(60), unique=True, nullable=False)

    # hospitalWorker = relationship("hospitalWorker", back_populates="hospitals")
