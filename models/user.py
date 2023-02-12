#!/usr/bin/python3
"""
user module
"""
from sqlalchemy import Column, Integer, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship

import sys
sys.path.insert(0, '..')


class user(BaseModel, Base):
    """
        user details
    """
    __tablename__ = "user"
    id        = Column(Integer, primary_key=True, unique=True, nullabe=False)
    name      = Column(String(128), unique=True, nullabe=False)
    phone     = Column(Integer,  unique=True, nullabe=False)
    email     = Column(String(128),unique=True, nullabe=False)
    userID    = Column(String(128), unique=True, nullabe=False)
    Address   = Column(String(128), unique=True, nullabe=False)
    password  = Column(String(128), unique=True, nullabe=False)
    
    
