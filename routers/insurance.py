from fastapi import APIRouter, Depends, status, HTTPException
from schema import showInsurance
from schema import insurance as insuranceSchema
from engine.loadb import load
from models import inusrance as insuranceModel
from sqlalchemy.orm import Session
from typing import Dict, List

router = APIRouter(
    tags=["insurance"]
)


@router.post("/insurance", response_model=showInsurance.ShowInsurance, status_code=status.HTTP_201_CREATED)
def create_insurance(request: insuranceSchema.Insurance, db: Session = Depends(load)):
    phone = request.phone
    insuranceID = request.insuranceID

    checkPhone = db.query_eng(insuranceModel.Insurance).filter(
        insuranceModel.Insurance.phone == phone).first()
    checkInsuranceID = db.query_eng(insuranceModel.Insurance).filter(
        insuranceModel.Insurance.insuranceID == insuranceID).first()

    if checkPhone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"company with phone: {phone} exists")
    if checkInsuranceID:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"company with Insurance ID: {insuranceID} exists")

    new_insurance = insuranceModel.Insurance(
        name=request.name, phone=request.phone, address=request.address, insuranceID=request.insuranceID)
    db.new(new_insurance)
    db.save()
    return new_insurance


@router.get("/insurance/all", response_model=List[showInsurance.ShowInsurance], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load)):
    companies = db.query_eng(insuranceModel.Insurance).all()
    return companies


@router.get("/insurance/{insuranceID}", response_model=showInsurance.ShowInsurance, status_code=status.HTTP_200_OK)
def show(insuranceID, db: Session = Depends(load)):
    company = db.query_eng(insuranceModel.Insurance).filter(
        insuranceModel.Insurance.insuranceID == insuranceID).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"company with the insurance ID: {insuranceID} not found")
    return company
