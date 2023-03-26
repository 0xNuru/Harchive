#!/usr/bin/python3
"""
insurance module
"""
import sys
sys.path.insert(0, '..')
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from models.base_model import BaseModel, Base
from models.user import Users



class InAdmin(Users):
    """ 
        Desc:
            admin details
    """
    __tablename__ = "InAdmin"
    id = Column(String, ForeignKey("user.id",  ondelete="CASCADE"),primary_key=True, nullable=False)
    insuranceID = Column(String, ForeignKey("Insurance.id",  ondelete="CASCADE"), nullable=False)
    role = Column(String(50), nullable=False, default='insurance_admin')
    Insurance = relationship("Insurance", back_populates="InAdmin")


class Insurance(BaseModel, Base):
    """
        insurance details
    """
    __tablename__ = "Insurance"
    # insuranceID = Column(String, ForeignKey(
    #     "InAdmin.insuranceID",  ondelete="CASCADE"), nullable=False)
    name = Column(String(128), nullable=False)
    address = Column(String(128), nullable=False)
    phone = Column(String(60), unique=True, nullable=False)
    InAdmin = relationship("InAdmin", back_populates="Insurance")
