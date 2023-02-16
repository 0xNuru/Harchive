#!/usr/bin/python3
"""
user module
"""
from sqlalchemy import Column, Integer, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship

import sys
sys.path.insert(0, '..')


class Users(BaseModel, Base):
    """
        user details
    """
    __tablename__ = "user"
    name = Column(String(128), nullable=False)
    phone = Column(String(60), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    address = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
