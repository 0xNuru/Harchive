from fastapi import APIRouter, Depends, status, HTTPException
from schema import showPatient
from schema import patient as patientSchema
from engine.loadb import load
from models import patient as patientModel
from sqlalchemy.orm import Session
from typing import Dict, List

router = APIRouter(
    tags=["patient"]
)


@router.post("/patient", response_model=showPatient.ShowPatient,
             status_code=status.HTTP_201_CREATED)
def create_patient(request: patientSchema.Patient, db: Session = Depends(load)):
    phone = request.phone
    email = request.email

    checkPhone = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.phone == phone).first()
    checkEmail = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.email == email).first()
    if checkPhone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"patient with phone: {phone} exists")
    if checkEmail:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"patient with email: {email} exists")

    new_patient = patientModel.Patient(name=request.name, phone=request.phone,
                                       email=request.email, address=request.address, password_hash=request.password, \
                                       insuranceID = request.insuranceID, dob=request.dob, gender=request.gender)
    db.new(new_patient)
    db.save()
    return new_patient


@router.get("/patient/all", response_model=List[showPatient.ShowPatient], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load)):
    patient = db.query_eng(patientModel.Patient).all()
    return patient


@router.get("/patient/{email}", response_model=showPatient.ShowPatient, status_code=status.HTTP_200_OK)
def show(email, db: Session = Depends(load)):
    patient = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.email == email).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with the email {email} not found")
    return patient
