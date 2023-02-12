#!/usr/bin/python3
"""
Record module
"""
import sys
sys.path.insert(0, '..')
from models.base_model import BaseModel, Base
from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, Float, DateTime, BOOLEAN, VARCHAR
from sqlalchemy.orm import relationship

class Record(BaseModel, Base):
    """
        Record details
    """
    __tablename__ = "record"
    id   = Column(Integer, primary_key=True, unique=True, nullabe=False)
    persons = relationship('Person', backref='record')
    DOB = Column(DateTime,    nullabe=False)
    Gender = Column(BOOLEAN, nullabe=False)
    BloodType = Column(VARCHAR(5), nullabe=False)
    Height = Column(Float, nullabe=False)
    weight = Column(Float, nullabe=False)
    BMI = Column(Float, nullabe=False)
    Allegies = Column(ARRAY, nullabe=False)
    Tests = Column(ARRAY, nullabe=False)
    Immunization = Column(ARRAY, nullabe=False)
    Medication = Column(ARRAY, nullabe=False)
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
    id   = Column(Integer, primary_key=True, unique=True, nullable=False)
    drug = Column(String(128), unique=True, nullable=False)
    amount = Column(Float, nullable=False)

