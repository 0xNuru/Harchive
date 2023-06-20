#!/usr/bin/python3


import sys
sys.path.insert(0, '..')
from loguru import logger
from utils.acl import check_role
from dependencies.depends import get_current_user
from fastapi import APIRouter, Depends, status, HTTPException
from schema.patient import ShowPatient
from schema import patient as patientSchema
from engine.loadb import load
from models import user as userModel
from models import patient as patientModel
from models import record as recordModel
from models import hospital as hospitalModel
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
                                       insuranceID=request.insuranceID, dob=request.dob, gender=request.gender, nin=request.nin)
    db.new(new_patient)
    db.save()
    return new_patient


@router.get("/all", response_model=List[ShowPatient], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load), user_data=Depends(get_current_user)):
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


@router.get("/record/nin/{nin}", response_model=patientSchema.PatientRecord, status_code=status.HTTP_200_OK)
def show(nin, user_data: get_current_user = Depends(), db: Session = Depends(load)):
    check_role('patient', user_data['user_id'])
    patient = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.nin == nin).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with the nin {nin} not found")
    id = patient.id
    record = db.query_eng(recordModel.Record).filter(
        recordModel.Record.patient == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with the nin {nin} does not have a record")
    return record


@router.put("/record/update/{nin}", response_model=patientSchema.PatientRecord)
def update_admin(nin, request: patientSchema.PatientRecord, user_data: get_current_user = Depends(), db: Session = Depends(load)):
    check_role('patient', user_data['user_id'])
    patient = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.nin == nin).first()

    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with nin: {nin} not found")
    id = patient.id
    record = db.query_eng(recordModel.Record).filter(
        recordModel.Record.patient == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with the nin {nin} does not have a record")
    record.type = request.type,
    record.patient = id,
    record.DOB = request.DOB,
    record.BloodType = request.BloodType,
    record.Height = request.Height,
    record.weight = request.weight,
    record.BMI = request.BMI

    updated_record = recordModel.Record(type=request.type, patient=id, DOB=request.DOB,
                                        BloodType=request.BloodType, Height=request.Height, weight=request.weight,
                                        BMI=request.BMI)
    db.save()
    return updated_record


@router.post("/medication/add/{nin}", response_model=patientSchema.ShowMedication,
             status_code=status.HTTP_201_CREATED)
def create_patient_medication(nin, request: patientSchema.Medication, user_data: get_current_user = Depends(), db: Session = Depends(load)):
    check_role('doctor', user_data['user_id'])
    id = user_data["user_id"]
    patient = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.nin == nin).first()
    doctor = db.query_eng(hospitalModel.Doctors).filter(
        hospitalModel.Doctors.id == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with the nin {nin} not found")

    new_medication = patientModel.Medication(medication_name=request.medication_name, patient=patient.id, hospitalID=doctor.hospitalID, dosage=request.dosage,
                                             doctor_id=id, start_date=request.start_date, due_date=request.due_date,
                                             reason=request.reason, doctor_name=user_data["username"])
    db.new(new_medication)
    db.save()
    return new_medication


@router.post("/allergy/add/{nin}", response_model=patientSchema.ShowAllergy,
             status_code=status.HTTP_201_CREATED)
def create_patient_allergy(nin, request: patientSchema.Allergy, user_data: get_current_user = Depends(), db: Session = Depends(load)):
    check_role('doctor', user_data['user_id'])
    id = user_data["user_id"]
    patient = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.nin == nin).first()
    doctor = db.query_eng(hospitalModel.Doctors).filter(
        hospitalModel.Doctors.id == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with the nin {nin} not found")

    new_allergy = patientModel.Allergy(allergy_name=request.allergy_name, patient=patient.id, hospitalID=doctor.hospitalID, reactions=request.reactions,
                                       doctor_id=id, more_info=request.more_info, type=request.type, doctor_name=user_data["username"])
    db.new(new_allergy)
    db.save()
    return new_allergy


@router.post("/immunization/add/{nin}", response_model=patientSchema.ShowImmunization,
             status_code=status.HTTP_201_CREATED)
def create_patient_immunization(nin, request: patientSchema.Immunization, user_data: get_current_user = Depends(), db: Session = Depends(load)):
    check_role('doctor', user_data['user_id'])
    id = user_data["user_id"]
    patient = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.nin == nin).first()
    doctor = db.query_eng(hospitalModel.Doctors).filter(
        hospitalModel.Doctors.id == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with the nin {nin} not found")

    new_immunization = patientModel.Immunization(patient=patient.id, name=request.name, hospitalID=doctor.hospitalID, immunization_date=request.immunization_date,
                                                 doctor_id=id, more_info=request.more_info, expiry_date=request.expiry_date, lot_number=request.lot_number, immunization_location=request.immunization_location, doctor_name=user_data["username"])
    db.new(new_immunization)
    db.save()
    return new_immunization


@router.post("/transaction/add/{nin}", response_model=patientSchema.Transaction,
             status_code=status.HTTP_201_CREATED)
def create_patient_transaction(nin, request: patientSchema.Transaction, user_data: get_current_user = Depends(), db: Session = Depends(load)):
    check_role('doctor', user_data['user_id'])
    id = user_data["user_id"]
    patient = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.nin == nin).first()
    doctor = db.query_eng(hospitalModel.Doctors).filter(
        hospitalModel.Doctors.id == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with the nin {nin} not found")

    new_immunization = patientModel.Transactions(patient=patient.id, hospitalID=doctor.hospitalID, doctor_id=id,
                                                 doctor_name=user_data["username"], description=request.description, quantity=request.quantity)
    db.new(new_immunization)
    db.save()
    return new_immunization
