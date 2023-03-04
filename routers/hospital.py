from fastapi import APIRouter, Depends, status, HTTPException
from schema import showHospital
from schema import hospital as hospitalSchema
from engine.loadb import load
from dependencies.depends import get_current_user
from models import hospital as hospitalModel
from sqlalchemy.orm import Session
from utils.acl import check_role
from typing import Dict, List


router = APIRouter(
    tags=["hospital"]
)


@router.post("/hospital", response_model=showHospital.ShowHospital, status_code=status.HTTP_201_CREATED)
def create_hospital(request: hospitalSchema.Hospital, db: Session = Depends(load)):
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
        name=request.name, phone=request.phone, address=request.address, hospitalID=request.hospitalID)
    db.new(new_hospital)
    db.save()
    return new_hospital


@router.get("/hospital/all", response_model=List[showHospital.ShowHospital], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load), user_data = Depends(get_current_user)):
    check_role('hospital_admin', user_data['user_id'])
    hospitals = db.query_eng(hospitalModel.Hospital).all()
    return hospitals


@router.get("/hospital/{hospitalID}", response_model=showHospital.ShowHospital, status_code=status.HTTP_200_OK)
def show(hospitalID, db: Session = Depends(load)):
    hospital = db.query_eng(hospitalModel.Hospital).filter(
        hospitalModel.Hospital.hospitalID == hospitalID).first()
    if not hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"hospital with the hospital ID: {hospitalID} not found")
    return hospital
