#!/usr/bin/python3
"""
Person module
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float

class Person(BaseModel, Base):
    """
        Person details
    """
    __tablename__ = "person"
    
    pass
