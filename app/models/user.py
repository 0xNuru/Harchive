#!/usr/bin/python3
"""
user module
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, DateTime, INTEGER
from models.base_model import BaseModel, Base
import sys
sys.path.insert(0, '..')


class Users(BaseModel, Base):
    """
        user details
    """
    __tablename__ = "user"
    name: str = Column(String(128), nullable=False,)
    phone: str = Column(String(60), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(50), nullable=True)
    is_verified =  Column(Boolean, nullable=True)
    failed_login_attempts = Column(INTEGER, nullable=False, default=0)
    is_suspended = Column(Boolean, nullable=True, default=False)
    suspended_at = Column(DateTime, nullable=True)
