#!/usr/bin/python3
"""
Record module
"""
# from graphene import Int
from sqlalchemy.orm import relationship
from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, Float, DateTime, BOOLEAN, VARCHAR
from models.base_model import BaseModel, Base
from datetime import datetime
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
    Allegies = relationship('Allergy', back_populates='record')
    Tests = relationship('Test', back_populates='record')
    Immunization = relationship('Immunization', back_populates='record')
    Medication = relationship('Medication', back_populates='record')
    Transactions = relationship('Transactions', back_populates='record')


class Transactions(BaseModel, Base):
    """
        Desc:
            record of transactions
        contains:
            - Drugs : list of drugs and costs
            - 


    """
    __tablename__ = "transactions"
    hospital_record_id = Column(String, ForeignKey('record.id'))
    Doctor = relationship('Doctor', backref='doctor.id')
    drug_name = Column(VARCHAR(255), nullable=False, unique=True)
    quantity = Column(VARCHAR(255), nullable=False, unique=True)
    transaction_amount = Column(VARCHAR(255), nullable=False, unique=True)
    transaction_type = Column(VARCHAR(255), nullable=False, unique=True)
    vendor_name = Column(VARCHAR(255), nullable=False, unique=True)
    transaction_date = Column(DateTime, nullable=False, default=(datetime.utcnow()))


class Medication(BaseModel, Base):
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
    medication_name = Column(String(128), unique=True, nullable=False)
    hospital_record_id = Column(String, ForeignKey('record.id'))
    Doctor = relationship('Doctor', backref='doctor.id')


class Test(BaseModel, Base):
    """
        Desc:
            contains tests

    """
    id = Column(Integer, primary_key=True, unique=True)
    test_name = Column(String, unique=True, nullable=False)
    scanned_test = None
    Doctor = relationship('Doctor', ForeignKey('doctor.id'))
    hospital_record_id = Column(String, ForeignKey('record.id'))


class Allergy(BaseModel, Base):
    """
        Desc:
            contains user allergy
    """
    id = Column(Integer, primary_key=True, unique=True)
    allergies = Column(String, unique=True, nullable=False)
    hospital_record_id = Column(String, ForeignKey('record.id'))

class Immunization(BaseModel, Base):
    """
        Desc:
            contains immunization detail history
    """
    id = Column(Integer, primary_key=True, unique=True)
    immunziation_name = Column(VARCHAR(255), nullable=False, unique=True)
    immunization_date = Column(DateTime, nullable=False, unique=True)
    immunization_location = Column(VARCHAR(255), nullable=False, unique=True)
    hospital_record_id = Column(String, ForeignKey('record.id'))
