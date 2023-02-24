#!/usr/bin/python3
"""
insurance module
"""
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from models.base_model import BaseModel, Base
from models.user import Users
import sys
sys.path.insert(0, '..')


class Insurance(BaseModel, Base):
    """
        insurance details
    """
    __tablename__ = "insurance"
    insuranceID = Column(String(128), nullable=False, unique=True)
    name = Column(String(128), nullable=False)
    address = Column(String(128), nullable=False)
    phone = Column(String(60), unique=True, nullable=False)
    admin = relationship("InAdmin", back_populates="insurance")
    


class InAdmin(Users):
    """ 
        Desc:
            admin details
    """
    __tablename__ = "Inadmin"
    id = Column(String, ForeignKey("user.id",  ondelete="CASCADE"),primary_key=True, nullable=False)
    inusranceID = Column(String, ForeignKey("insurance.id",  ondelete="CASCADE"), nullable=False)
    role = Column(String(50), nullable=False, default='insurance_admin')
    insurance = relationship("Insurance")