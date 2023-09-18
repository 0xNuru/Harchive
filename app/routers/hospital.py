#!/usr/bin/python3


from pydantic import EmailStr
from utils import auth
from models import user as userModel
from typing import Dict, List
from utils.acl import check_role
from sqlalchemy.orm import Session
from models import patient as patientModel
from models import hospital as hospitalModel
from dependencies.depends import get_current_user
from engine.loadb import load
from schema import hospital as hospitalSchema
from loguru import logger
from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
import sys
sys.path.insert(0, '..')


router = APIRouter(
    prefix="/hospital",
    tags=["hospital"]
)


@router.post("/admin/register", response_model=hospitalSchema.ShowHospital, status_code=status.HTTP_201_CREATED)
def create_hospital_admin(request: hospitalSchema.HospitalAdmin, db: Session = Depends(load),user_data=Depends(get_current_user)):
    roles = ["superuser"]
    check_role(roles, user_data['user_id'])
    phone = request.phone
    hospitalID = request.hospitalID
    email = request.email

    checkPhone = db.query_eng(userModel.Users).filter(
        userModel.Users.phone == phone).first()
    checkEmail = db.query_eng(userModel.Users).filter(
        userModel.Users.email == email).first()
    checkhospitalID = db.query_eng(hospitalModel.Admin).filter(
        hospitalModel.Admin.hospitalID == hospitalID).first()

    if checkPhone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"hospital with phone: {phone} exists")
    if checkEmail:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"hospital with email: {email} exists")
    if checkhospitalID:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"hospital with hospital ID: {hospitalID} exists")

    passwd_hash = auth.get_password_hash(request.password2.get_secret_value())

    new_hospital_admin = hospitalModel.Admin(
        name=request.name, phone=request.phone, email=request.email, password_hash=passwd_hash, hospitalID=request.hospitalID, role="hospital_admin")
    db.new(new_hospital_admin)
    db.save()
    return new_hospital_admin


@router.get("/admin/all", response_model=List[hospitalSchema.ShowHospital], status_code=status.HTTP_200_OK)
def all_admins(db: Session = Depends(load), user_data=Depends(get_current_user)):
    roles = ["hospital_admin"]
    check_role(roles, user_data['user_id'])
    admins = db.query_eng(hospitalModel.Admin).all()
    return admins


@router.get("/admin/hospitalID/{hospitalID}",
            response_model=hospitalSchema.ShowHospital, status_code=status.HTTP_200_OK)
def show_admin(hospitalID, db: Session = Depends(load),
               user_data=Depends(get_current_user)):
    roles = ["hospital_admin"]
    check_role(roles, user_data['user_id'])
    admin = db.query_eng(hospitalModel.Admin).filter(
        hospitalModel.Admin.hospitalID == hospitalID).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with the hospital ID: {hospitalID} not found")
    return admin


@router.delete("/admin/delete/{hospitalID}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hospital_admin(hospitalID, db: Session = Depends(load), user_data=Depends(get_current_user)):
    roles = ["hospital_admin"]
    check_role(roles, user_data['user_id'])
    admin = db.query_eng(hospitalModel.Admin).filter(
        hospitalModel.Admin.hospitalID == hospitalID).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin with id {hospitalID} not found")
    db.delete(admin)
    db.save()
    return {"data": "Deleted!"}


@router.post("/register", response_model=hospitalSchema.ShowHospital,
             status_code=status.HTTP_201_CREATED)
def create_hospital(request: hospitalSchema.Hospital,
                    db: Session = Depends(load), user_data=Depends(get_current_user)):
    roles = ["hospital_admin"]
    check_role(roles, user_data['user_id'])
    phone = request.phone
    hospitalID = request.hospitalID

    checkPhone = db.query_eng(hospitalModel.Hospital).filter(
        hospitalModel.Hospital.phone == phone).first()
    checkhospitalID = db.query_eng(hospitalModel.Hospital).filter(
        hospitalModel.Hospital.hospitalID == hospitalID).first()

    if checkPhone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"hospital with phone: {phone} exists")
    if checkhospitalID:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"hospital with hospital ID: {hospitalID} exists")

    new_hospital = hospitalModel.Hospital(
        name=request.name, phone=request.phone,
        hospitalID=request.hospitalID, address=request.address)
    db.new(new_hospital)
    db.save()
    return new_hospital


@router.get("/all", response_model=List[hospitalSchema.ShowHospital], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load), user_data=Depends(get_current_user)):
    roles = ["hospital_admin"]
    check_role(roles, user_data['user_id'])
    hospitals = db.query_eng(hospitalModel.Hospital).all()
    return hospitals


@router.get("/{hospitalID}", response_model=hospitalSchema.ShowHospital, status_code=status.HTTP_200_OK)
def show(hospitalID, db: Session = Depends(load), user_data=Depends(get_current_user)):
    roles = ["hospital_admin"]
    check_role(roles, user_data['user_id'])
    hospital = db.query_eng(hospitalModel.Hospital).filter(
        hospitalModel.Hospital.hospitalID == hospitalID).first()
    if not hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"hospital with the hospital ID: {hospitalID} not found")
    return hospital


@router.post("/doctor/register", response_model=hospitalSchema.ShowDoctor,
             status_code=status.HTTP_201_CREATED)
def create_doctor(request: hospitalSchema.Doctor, db: Session = Depends(load), user_data=Depends(get_current_user)):
    roles = ["hospital_admin"]
    check_role(roles, user_data['user_id'])
    admin_id = user_data["user_id"]
    admin = db.query_eng(hospitalModel.Admin).filter(
        hospitalModel.Admin.id == admin_id).first()
    
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

    new_doctor = hospitalModel.Doctors(name=request.name, phone=request.phone,
                                       email=request.email, password_hash=passwd_hash,
                                       hospitalID=admin.hospitalID, dob=request.dob, gender=request.gender, speciality=request.speciality, role="doctor")
    db.new(new_doctor)
    db.save()
    return new_doctor


@router.get("/doctor/all", response_model=List[hospitalSchema.ShowDoctor], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load), user_data=Depends(get_current_user)):
    roles = ["hospital_admin"]
    check_role(roles, user_data['user_id'])
    doctor = db.query_eng(hospitalModel.Doctors).all()
    return doctor


@router.get("/doctor/email/{email}",
            response_model=hospitalSchema.ShowDoctor, status_code=status.HTTP_200_OK)
def show(email: EmailStr, db: Session = Depends(load), user_data=Depends(get_current_user)):
    roles = ["hospital_admin"]
    check_role(roles, user_data['user_id'])
    doctor = db.query_eng(hospitalModel.Doctors).filter(
        hospitalModel.Doctors.email == email).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"doctor with the email {email} not found")
    return doctor


@router.delete("/doctor/delete/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(email: EmailStr, db: Session = Depends(load),   user_data=Depends(get_current_user)):
    roles = ["hospital_admin"]
    check_role(roles, user_data['user_id'])
    doctor = db.query_eng(hospitalModel.Doctors).filter(
        hospitalModel.Doctors.email == email).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"doctor with email: {email} not found")
    db.delete(doctor)
    db.save()
    return {"data": "Deleted!"}


@router.post("/checkIn", status_code=status.HTTP_201_CREATED)
def check_in(request: hospitalSchema.CheckIn, db: Session = Depends(load), user_data=Depends(get_current_user)):
    roles = ["hospital_admin"]
    check_role(roles, user_data['user_id'])
    admin_id = user_data["user_id"]
    patient = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.nin == request.nin).first()
    admin = db.query_eng(hospitalModel.Admin).filter(
        hospitalModel.Admin.id == admin_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with the nin {request.nin} not found")

    checkHospital = db.query_eng(hospitalModel.Hospital).filter(hospitalModel.Hospital.hospitalID == admin.hospitalID).first()
    if not checkHospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Hospital with ID '{admin.hospitalID}' not found")

    checkPatient = db.query_eng(hospitalModel.CheckIn).filter(
        hospitalModel.CheckIn.patient == patient.id).first()
    checkHID = db.query_eng(hospitalModel.CheckIn).filter(
        hospitalModel.CheckIn.hospitalID == admin.hospitalID).first()
    if checkPatient and checkHID:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"This patient is already checked into this hospital")

    new_check_in = hospitalModel.CheckIn(
        patient=patient.id, hospitalID=admin.hospitalID)
    db.new(new_check_in)
    db.save()
    return new_check_in


@router.delete("/checkout", status_code=status.HTTP_204_NO_CONTENT)
def check_out(request: hospitalSchema.CheckIn, db: Session = Depends(load), user_data=Depends(get_current_user)):
    roles = ["hospital_admin"]
    check_role(roles, user_data['user_id'])
    patient = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.nin == request.nin).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with the nin {request.nin} not found")
    check_in = db.query_eng(hospitalModel.CheckIn).filter(
        hospitalModel.CheckIn.patient == patient.id).first()

    db.delete(check_in)
    db.save()
    return {"data": "checked-out!"}
