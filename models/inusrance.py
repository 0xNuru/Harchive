#!/usr/bin/python3
"""
insurance module
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float

class Insurance(BaseModel, Base):
    """
        insurance details
    """
    __tablename__ = "insurance"
    
    pass