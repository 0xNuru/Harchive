#!/usr/bin/python3
"""
Record module
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float

class Record(BaseModel, Base):
    """
        Record details
    """
    __tablename__ = "record"
    pass