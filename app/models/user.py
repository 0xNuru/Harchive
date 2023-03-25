#!/usr/bin/python3
"""
user module
"""
from sympy import chebyshevt
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Enum, CheckConstraint
from sqlalchemy.orm import relationship


import sys
sys.path.insert(0, '..')


class Users(BaseModel, Base):
    """
        user details
    """
    __tablename__ = "user"
    name : str = Column(String(128), nullable=False,)
    phone : str = Column(String(60), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

