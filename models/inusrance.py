#!/usr/bin/python3
"""
insurance module
"""
import sys
sys.path.insert(0, '..')

from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

class Insurance(BaseModel, Base):
    """
        insurance details
    """
    __tablename__ = "insurance"
    id   = Column(Integer, primary_key=True, unique=True, nullabe=False)
    insuranceID = Column(String(128), nullabe=False, unique=True)
    admin = relationship('Person', backref='insurance')
