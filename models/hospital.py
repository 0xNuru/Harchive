#!/usr/bin/python3
"""
Hospital module

"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float

class Hospital(BaseModel, Base):
    """
        hospital details
    """
    __tablename__ = "hospital"
    
    pass