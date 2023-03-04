from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from schema import hospital as hospitalSchema
from engine.loadb import load
from dependencies.depends import get_current_user
from models import hospital as hospitalModel
from sqlalchemy.orm import Session
from utils.acl import check_role
from typing import Dict, List
from models import user as userModel
from utils import auth
from utils.oauth1 import AuthJWT
from models import user as userModel


from utils import auth


router = APIRouter(
    prefix="/hospital",
    tags=["hospital"]
)


@router.post("/admin/register", response_model=hospitalSchema.ShowHospital, status_code=status.HTTP_201_CREATED)
def create_hospital_admin(request: hospitalSchema.HospitalAdmin, db: Session = Depends(load)):
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
        name=request.name, phone=request.phone, email=request.email, password_hash=passwd_hash, hospitalID=request.hospitalID)
    db.new(new_hospital_admin)
    db.save()
    return new_hospital_admin


@router.get("/admin/all", response_model=List[hospitalSchema.ShowHospital], status_code=status.HTTP_200_OK)
def all_admins(db: Session = Depends(load), user_data = Depends(get_current_user) ):
    check_role('hospital_admin', user_data['user_id'])
    admins = db.query_eng(hospitalModel.Admin).all()
    return admins


@router.get("/admin/hospitalID/{hospitalID}",
         response_model=hospitalSchema.ShowHospital, status_code=status.HTTP_200_OK)
def show_admin(hospitalID, db: Session = Depends(load), 
                user_data = Depends(get_current_user)):
    check_role('hospital_admin', user_data['user_id'])
    admin = db.query_eng(hospitalModel.Admin).filter(
        hospitalModel.Admin.hospitalID == hospitalID).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with the hospital ID: {hospitalID} not found")
    return admin



@router.post("/register", response_model=hospitalSchema.ShowHospital, 
                                    status_code=status.HTTP_201_CREATED)
def create_hospital(request: hospitalSchema.Hospital, 
                    db: Session = Depends(load), user_data = Depends(get_current_user)):
    check_role('hospital_admin', user_data['user_id'])
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
def all(db: Session = Depends(load), user_data = Depends(get_current_user)):
    check_role('hospital_admin', user_data['user_id'])
    hospitals = db.query_eng(hospitalModel.Hospital).all()
    return hospitals


@router.get("/{hospitalID}", response_model=hospitalSchema.ShowHospital, status_code=status.HTTP_200_OK)
def show(hospitalID, db: Session = Depends(load), user_data = Depends(get_current_user)):
    check_role('hospital_admin', user_data['user_id'])
    hospital = db.query_eng(hospitalModel.Hospital).filter(
        hospitalModel.Hospital.hospitalID == hospitalID).first()
    if not hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"hospital with the hospital ID: {hospitalID} not found")
    return hospital


@router.post("/doctor/register", response_model=hospitalSchema.ShowDoctor,
             status_code=status.HTTP_201_CREATED)
def create_doctor(request: hospitalSchema.Doctor, db: Session = Depends(load)):
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

    new_doctor = hospitalModel.Doctor(name=request.name, phone=request.phone,
                                      email=request.email, address=request.address, password_hash=passwd_hash,
                                      hospitalID=request.hospitalID, dob=request.dob, gender=request.gender)
    db.new(new_doctor)
    db.save()
    return new_doctor


@router.get("/doctor/all", response_model=List[hospitalSchema.ShowDoctor], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load), user_data = Depends(get_current_user)):
    check_role('doctor', user_data['user_id'])
    doctor = db.query_eng(hospitalModel.Doctor).all()
    return doctor


@router.get("/doctor/email/{email}", 
            response_model=hospitalSchema.ShowDoctor, status_code=status.HTTP_200_OK)
def show(email, db: Session = Depends(load), user_data = Depends(get_current_user)):
    check_role('doctor', user_data['user_id'])
    doctor = db.query_eng(hospitalModel.Doctor).filter(
        hospitalModel.Doctor.email == email).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"doctor with the email {email} not found")
    return doctor
