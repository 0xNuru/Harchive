#!/usr/bin/python3
"""
Record module
"""
from sqlalchemy.orm import relationship
from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, Float, DateTime, BOOLEAN, VARCHAR
from models.base_model import BaseModel, Base
import sys
sys.path.insert(0, '..')


class Record(BaseModel, Base):
    """
        Record details
    """
    __tablename__ = "record"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    user = relationship('User', backref='record')
    DOB = Column(DateTime,    nullable=False)
    Gender = Column(BOOLEAN, nullable=False)
    BloodType = Column(VARCHAR(5), nullable=False)
    Height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    BMI = Column(Float, nullable=False)
    Allegies = Column(ARRAY, nullable=False)
    Tests = Column(ARRAY, nullable=False)
    Immunization = Column(ARRAY, nullable=False)
    Medication = Column(ARRAY, nullable=False)
    transactions = relationship('Transactions', backref='record')


class Transactions(BaseModel, Base):
    """
        Desc:
            record of transactions
        contains:
            - Drugs : list of drugs and costs
            - 


    """
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Drugs = relationship('Drugs', backref='transactions')


class Drugs(BaseModel, Base):
    """
        Desc:
            contains drug and cost
        contains:
            - id     : unique identifier
            - drug   : name of drug
            - amount : cost
    """
    __tablename__ = "drugs"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    drug = Column(String(128), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
