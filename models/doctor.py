#!/usr/bin/python3
"""
doctor module

"""
import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum, null
from models.user import Users
from sqlalchemy.orm import relationship


class genderEnum(enum.Enum):
    M = "M"
    F = "F"


class Doctor(Users):
    """
        doctor details
    """
    __tablename__ = "doctor"
    id = Column(String, ForeignKey(
        'user.id',  ondelete="CASCADE"), primary_key=True)
    hospitalID = Column(String(128), nullable=True)
    address = Column(String(128), nullable=False)
    role = Column(String(50), nullable=False, default='doctor')
