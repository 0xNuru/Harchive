#!/usr/bin/python3
"""
user module
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Enum, CheckConstraint, ForeignKey
from models.base_model import BaseModel, Base
from sympy import chebyshevt
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
    role = Column(String(50), nullable=False)

class Superuser(Users):
    """ 
        Desc:
            superuser details
    """
    __tablename__ = "superuser"
    id = Column(String, ForeignKey("user.id",  ondelete="CASCADE"),
                primary_key=True, nullable=False)
    