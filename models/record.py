#!/usr/bin/python3
"""
Record module
"""
# from graphene import Int
import enum
from sqlalchemy.orm import relationship
from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, Float, DateTime, BOOLEAN, VARCHAR, Enum
from models.base_model import BaseModel, Base
from models.hospital import *
from datetime import datetime
import sys
sys.path.insert(0, '..')


class allergyEnum(enum.Enum):
    FOOD = "FOOD"
    DRUG = "DRUG"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    INSECT = "INSECT"
    LATEX = "LATEX"
    CONTACT = "CONTACT"
    WEATHER = "WEATHER"


class Transactions(BaseModel, Base):
    """
        Desc:
            record of transactions
        contains:
            - Drugs : list of drugs and costs
            - 


    """
    __tablename__ = "transactions"

    doctor_id = Column(String, ForeignKey(
        'doctors.id',  ondelete="CASCADE"), nullable=False)
    description = Column(VARCHAR(255), nullable=False, unique=True)
    quantity = Column(VARCHAR(255), nullable=False, unique=True)
    hospitalID = Column(String, ForeignKey("hospital.hospitalID"))
    patient = Column(String, ForeignKey('patient.id', ondelete="CASCADE"))
    Doctor = relationship('Doctors', back_populates='transactions')


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

    medication_name = Column(String(128), unique=False, nullable=False)
    patient = Column(String, ForeignKey('patient.id', ondelete="CASCADE"))
    dosage = Column(String, nullable=True)
    doctor_id = Column(String, ForeignKey(
        'doctors.id',  ondelete="CASCADE"), nullable=False)
    hospitalID = Column(String, ForeignKey("hospital.hospitalID"))
    start_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    reason = Column(String, nullable=True)
    Doctor = relationship('Doctors', back_populates='medications')


class Test(BaseModel, Base):
    """
        Desc:
            contains tests

    """
    __tablename__ = "test"

    test_name = Column(String, unique=True, nullable=False)
    scanned_test = None
    doctor_id = Column(String, ForeignKey(
        'doctors.id',  ondelete="CASCADE"), nullable=False)
    Doctor = relationship('Doctors', back_populates='test')
    hospital_record_id = Column(
        String, ForeignKey('record.id',  ondelete="CASCADE"))


class Allergy(BaseModel, Base):
    """
        Desc:
            contains user allergy
    """
    __tablename__ = "allergy"

    allergy_name = Column(String, unique=False, nullable=False)
    patient = Column(String, ForeignKey('patient.id', ondelete="CASCADE"))
    type = Column(Enum(allergyEnum, name="allergy_enum"),
                  nullable=False, unique=False)
    reactions = Column(String, unique=False, nullable=False)
    hospitalID = Column(String, ForeignKey("hospital.hospitalID"))
    more_info = Column(String, unique=False, nullable=False)
    doctor_id = Column(String, ForeignKey(
        'doctors.id',  ondelete="CASCADE"), nullable=False)
    doctor = relationship("Doctors", back_populates="allergies")


class Immunization(BaseModel, Base):
    """
        Desc:
            contains immunization detail history
    """
    __tablename__ = "immunization"

    name = Column(VARCHAR(255), nullable=False, unique=False)
    immunization_date = Column(DateTime, nullable=False, unique=False)
    expiry_date = Column(DateTime, nullable=False, unique=False)
    immunization_location = Column(VARCHAR(255), nullable=False, unique=False)
    lot_number = Column(VARCHAR(255), nullable=False, unique=False)
    patient = Column(String, ForeignKey('patient.id', ondelete="CASCADE"))
    hospitalID = Column(String, ForeignKey("hospital.hospitalID"))
    more_info = Column(String, unique=False, nullable=False)
    doctor_id = Column(String, ForeignKey(
        'doctors.id',  ondelete="CASCADE"), nullable=False)
    doctor = relationship("Doctors", back_populates="immunizations")


class Record(BaseModel, Base):
    """
        Record details
    """
    __tablename__ = "record"
    patient = Column(String, ForeignKey('patient.id', ondelete="CASCADE"))
    type = Column(String(50))
    DOB = Column(DateTime,    nullable=False)
    BloodType = Column(VARCHAR(5), nullable=False)
    Height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    BMI = Column(Float, nullable=False)
    test_record = relationship(Test, backref='record')

    # __mapper_args__ = {
    #     'polymorphic_identity': 'record',
    #     'polymorphic_on': type
    # }
