#!/usr/bin/python3
"""
Record module
"""
# from graphene import Int
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, Float, DateTime, BOOLEAN, VARCHAR
from models.base_model import BaseModel, Base
from models.hospital import *
from datetime import datetime
import sys
sys.path.insert(0, '..')



class Transactions(BaseModel, Base):
    """
        Desc:
            record of transactions
        contains:
            - Drugs : list of drugs and costs
            - 


    """
    __tablename__ = "transactions"
    hospital_record_id = Column(String, ForeignKey('record.id',  ondelete="CASCADE"))
    doctor_id = Column(String, ForeignKey('doctors.id',  ondelete="CASCADE"), nullable=False)
    Doctor = relationship('Doctor', back_populates='transactions')
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
    __tablename__ = "medications"
   
    medication_name = Column(String(128), unique=True, nullable=False)
    hospital_record_id = Column(String, ForeignKey('record.id',  ondelete="CASCADE"))
    doctor_id = Column(String, ForeignKey('doctors.id',  ondelete="CASCADE"), nullable=False)
    Doctor = relationship('Doctor', back_populates='medications')


class Test(BaseModel, Base):
    """
        Desc:
            contains tests

    """
    __tablename__ = "test"
   
    test_name = Column(String, unique=True, nullable=False)
    scanned_test = None
    doctor_id = Column(String, ForeignKey('doctors.id',  ondelete="CASCADE"), nullable=False)
    Doctor = relationship('Doctor', back_populates='test')
    hospital_record_id = Column(String, ForeignKey('record.id',  ondelete="CASCADE"))


class Allergy(BaseModel, Base):
    """
        Desc:
            contains user allergy
    """
    __tablename__ = "allergy"
   
    allergies = Column(String, unique=True, nullable=False)
    hospital_record_id = Column(String, ForeignKey('record.id',  ondelete="CASCADE"))

class Immunization(BaseModel, Base):
    """
        Desc:
            contains immunization detail history
    """
    __tablename__ = "immunization"
   
    immunziation_name = Column(VARCHAR(255), nullable=False, unique=True)
    immunization_date = Column(DateTime, nullable=False, unique=True)
    immunization_location = Column(VARCHAR(255), nullable=False, unique=True)
    hospital_record_id = Column(String, ForeignKey('record.id',  ondelete="CASCADE"))



class Record(BaseModel, Base):
    """
        Record details
    """
    __tablename__ = "record"
    patient = Column(String,ForeignKey('patient.id',ondelete="CASCADE"))
    type = Column(String(50))
    DOB = Column(DateTime,    nullable=False)
    BloodType = Column(VARCHAR(5), nullable=False)
    Height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    BMI = Column(Float, nullable=False)
    allergy_record = relationship(Allergy, backref='record')
    test_record = relationship(Test,backref='record')
    immunization_record = relationship(Immunization, backref='record')
    medication_record = relationship(Medication, backref='record')
    transactions_record = relationship(Transactions, backref='record')

    __mapper_args__ = {
        'polymorphic_identity': 'record',
        'polymorphic_on': type
    }
