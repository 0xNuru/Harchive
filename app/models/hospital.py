#!/usr/bin/python3
"""
Hospital module

"""

import sys
sys.path.insert(0, '..')

from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from models.user import Users



class Admin(Users):
    """ 
        Desc:
            admin details
    """
    __tablename__ = "admin"
    id = Column(String, ForeignKey("user.id",  ondelete="CASCADE"),
                primary_key=True, nullable=False)
    hospitalID = Column(String(128), nullable=False, unique=True)
    role = Column(String(50), nullable=False, default='hospital_admin')
    hospital = relationship("Hospital", back_populates="admin")
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
        #  ,
        # 'inherit_condition': 'admin' == 'user'
    }


class Hospital(BaseModel, Base):
    """
        Desc:
            hospital details
    """
    __tablename__ = "hospital"
    hospitalID = Column(String, ForeignKey(
        "admin.hospitalID",  ondelete="CASCADE"), nullable=False, primary_key=True, unique=True)
    name = Column(String(128), nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    admin = relationship("Admin", back_populates="hospital")
    workers = relationship(
        "HospitalWorker", back_populates="hospital", cascade='all, delete-orphan')
    medication = relationship("Medication", cascade_backrefs='hospitalID')
    allergy = relationship("Allergy", cascade_backrefs='hospitalID')
    checkIn = relationship("CheckIn", cascade_backrefs='hospitalID')

    # doctors = relationship(
    #     "Doctor", back_populates="hospital", cascade='all, delete-orphan')


class HospitalWorker(BaseModel, Base):
    """
        Desc:
            hospitalWorker details
    """
    __tablename__ = "hospitalWorkers"
    id = Column(String, primary_key=True, nullable=False)
    hospitalID = Column(String, ForeignKey(
        "hospital.id",  ondelete="CASCADE"), nullable=False)
    doctors = relationship("Doctors", back_populates="worker")
    hospital = relationship("Hospital", back_populates="workers")


class Doctors(Users):
    """
        Desc:
            Doctor details
    """
    __tablename__ = "doctors"
    id = Column(String, ForeignKey("user.id",  ondelete="CASCADE"),
                primary_key=True, nullable=False)
    speciality = Column(String, nullable=True)
    hospitalID = Column(String, ForeignKey(
        "hospitalWorkers.id"), nullable=False)
    role = Column(String(50), nullable=False, default='doctor')
    worker = relationship("HospitalWorker", back_populates="doctors")
    transactions = relationship('Transactions', back_populates='Doctor',
                                primaryjoin='Doctors.id == Transactions.doctor_id')
    medications = relationship('Medication', back_populates='Doctor',
                               primaryjoin='Doctors.id == Medication.doctor_id')
    allergies = relationship("Allergy", back_populates="doctor")
    immunizations = relationship("Immunization", back_populates="doctor")
    test = relationship('Test', back_populates='Doctor',
                        primaryjoin='Doctors.id == Test.doctor_id')
    __mapper_args__ = {
        'polymorphic_identity': 'doctor',
        # 'inherit_condition': 'doctors' == 'user'
    }


class CheckIn(BaseModel, Base):
    """
        Desc:
            table for checked-in patients and the hospital(s) they are checked into
    """
    __tablename__ = "checkIn"
    patient = Column(String, ForeignKey(
        'patient.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    hospitalID = Column(String, ForeignKey(
        "hospital.hospitalID"), nullable=False)
