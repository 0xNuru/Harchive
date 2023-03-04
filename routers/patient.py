#!/usr/bin/python3

from utils.acl import check_role
from dependencies.depends import get_current_user
from fastapi import APIRouter, Depends, status, HTTPException
from schema.patient import ShowPatient
from schema import patient as patientSchema
from engine.loadb import load
from models import user as userModel
from models import patient as patientModel
from models import record as recordModel
from sqlalchemy.orm import Session
from typing import Dict, List
from utils import auth
from models import user as userModel





router = APIRouter(
    prefix="/patient",
    tags=["patient"]
)


@router.post("/register", response_model=patientSchema.ShowPatient,
             status_code=status.HTTP_201_CREATED)
def create_patient(request: patientSchema.Patient, db: Session = Depends(load)):
    phone = request.phone
    email = request.email

    checkPhone = db.query_eng(userModel.Users).filter(
        userModel.Users.phone == phone).first()
    checkEmail = db.query_eng(userModel.Users).filter(
        userModel.Users.email == email).first()
    if checkPhone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"user with phone: {phone} exists")
    if checkEmail:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"user with email: {email} exists")

    passwd_hash = auth.get_password_hash(request.password2.get_secret_value())

    new_patient = patientModel.Patient(name=request.name, phone=request.phone,
                                       email=request.email, address=request.address, password_hash=passwd_hash,
                                       insuranceID=request.insuranceID, dob=request.dob, gender=request.gender)
    db.new(new_patient)
    db.save()
    return new_patient


@router.get("/all", response_model=List[ShowPatient], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load), user_data = Depends(get_current_user)):
    check_role('patient', user_data['user_id'])
    patient = db.query_eng(patientModel.Patient).all()
    return patient


@router.get("/email/{email}", response_model=patientSchema.ShowPatient, status_code=status.HTTP_200_OK)
def show(email, db: Session = Depends(load), user_data: get_current_user = Depends()):
    check_role('patient', user_data['user_id'])
    patient = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.email == email).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with the email {email} not found")
    return patient



@router.post("/record/add", response_model=patientSchema.PatientRecord,
             status_code=status.HTTP_201_CREATED)
def create_patient_record(request: patientSchema.PatientRecord, user_data: get_current_user = Depends(), db: Session = Depends(load)):
    check_role('patient', user_data['user_id'])
    id = user_data["user_id"]
    check = db.query_eng(recordModel.Record).filter(
        recordModel.Record.patient == id).first()
    if check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"record for this patient exists")

    new_record = recordModel.Record(type=request.type, patient=id, DOB=request.DOB,
                                    BloodType=request.BloodType, Height=request.Height, weight=request.weight,
                                    BMI=request.BMI)
    db.new(new_record)
    db.save()
    return new_record


@router.get("/record/all", response_model=List[patientSchema.PatientRecord], status_code=status.HTTP_200_OK)
def all(user_data: get_current_user = Depends(), db: Session = Depends(load)):
    check_role('patient', user_data['user_id'])
    records = db.query_eng(recordModel.Record).all()
    return records


@router.get("/record/email/{email}", response_model=patientSchema.PatientRecord, status_code=status.HTTP_200_OK)
def show(email, user_data: get_current_user = Depends(), db: Session = Depends(load)):
    check_role('patient', user_data['user_id'])
    patient = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.email == email).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with the email {email} not found")
    id = patient.id
    record = db.query_eng(recordModel.Record).filter(
        recordModel.Record.patient == id).first()
    return record
