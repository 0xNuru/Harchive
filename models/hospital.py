#!/usr/bin/python3
"""
Hospital module

"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from models.user import Users
import sys
sys.path.insert(0, '..')


class Hospital(BaseModel, Base):
    """
        hospital details
    """
    __tablename__ = "hospital"
    name = Column(String(128), nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    hospitalID = Column(String(128), nullable=False)
    workers = relationship("HospitalWorker", back_populates="hospital", cascade='all, delete-orphan')


class HospitalWorker(BaseModel, Base):
    """
        hospitalWorker details
    """
    __tablename__ = "hospitalWorkers"
    id = Column(String,primary_key=True, nullable=False)
    hospitalID = Column(String, ForeignKey("hospital.id",  ondelete="CASCADE"), nullable=False)

    doctors = relationship("Doctor", back_populates="worker")
    admin = relationship("Admin", back_populates="worker")
    hospital = relationship("Hospital", back_populates="workers")



class Doctor(Users):
    """
        Doctor details
    """
    __tablename__ = "doctors"
    id = Column(String, ForeignKey("user.id",  ondelete="CASCADE"),primary_key=True, nullable=False)
    speciality = Column(String, nullable=False)
    hospitalID = Column(String, ForeignKey("hospitalWorkers.id"), nullable=False)
    worker = relationship("HospitalWorker", back_populates="doctors")
    transactions = relationship('Transactions', back_populates='Doctor',\
    primaryjoin='Doctor.id == Transactions.doctor_id')
    medications = relationship('Medication', back_populates='Doctor',\
    primaryjoin='Doctor.id == Medication.doctor_id')
    test = relationship('Test', back_populates='Doctor',\
    primaryjoin='Doctor.id == Test.doctor_id')
    __mapper_args__ = {
        'polymorphic_identity': 'doctor',
        # 'inherit_condition': 'doctors' == 'user'
    }

class Admin(Users):
    """
        Doctor details
    """
    __tablename__ = "admin"
    id = Column(String, ForeignKey("user.id",  ondelete="CASCADE"),primary_key=True, nullable=False)
    hospitalID = Column(String, ForeignKey("hospitalWorkers.id",  ondelete="CASCADE"), nullable=False)
    worker = relationship("HospitalWorker", back_populates="admin")
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
        #  ,
        # 'inherit_condition': 'admin' == 'user'
    }


