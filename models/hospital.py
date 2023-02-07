#!/usr/bin/python3
"""
Hospital module

"""
import sys
sys.path.insert(0, '..')
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float

class Hospital(BaseModel, Base):
    """
        hospital details
    """
    __tablename__ = "hospital"
    id   = Column(Integer, primary_key=True, unique=True, nullabe=False)
    name = Column(String(128), nullabe=False)
    pass