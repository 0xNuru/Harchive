#!/usr/bin/python3

"""End point routes for insurance company"""


from utils import auth
from utils.acl import check_role
from typing import Dict, List
from sqlalchemy.orm import Session
from models import insurance as insuranceModel
from engine.loadb import load
from schema import insurance as insuranceSchema
from schema.insurance import ShowInsurance
from fastapi import APIRouter, Depends, status, HTTPException, Request
from dependencies.depends import get_current_user
from utils.email import verifyEmail
import sys
sys.path.insert(0, '..')


router = APIRouter(
    prefix="/insurance",
    tags=["insurance"]
)


@router.post("/admin/register", response_model=insuranceSchema.ShowInsurance, status_code=status.HTTP_201_CREATED)
async def create_in_admin(request: insuranceSchema.InAdmin, http_request: Request, db: Session = Depends(load)):
    phone = request.phone
    insuranceID = request.insuranceID.lower()
    email = request.email.lower()

    checkPhone = db.query_eng(insuranceModel.InAdmin).filter(
        insuranceModel.InAdmin.phone == phone).first()
    checkInsuranceID = db.query_eng(insuranceModel.InAdmin).filter(
        insuranceModel.InAdmin.insuranceID == insuranceID).first()

    if checkPhone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Insurance admin with phone: {phone} exists")
    if checkInsuranceID:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Insurance admin with Insurance ID: {insuranceID} exists")
    
    await verifyEmail(email, http_request, request)

    passwd_hash = auth.get_password_hash(request.password2.get_secret_value())

    new_inAdmin = insuranceModel.InAdmin(
        name=request.name,
        phone=request.phone,
        email=email,
        password_hash=passwd_hash,
        insuranceID=insuranceID,
        role="insurance_admin")

    db.new(new_inAdmin)
    db.save()
    
    return {
        "name": request.name,
        "email": email,
        "role": new_inAdmin.role,
        "message": "Verification email sent successfully"}


@router.get("/admin/all", response_model=List[insuranceSchema.ShowInsurance], status_code=status.HTTP_200_OK)
def all_admins(db: Session = Depends(load), user_data: get_current_user = Depends()):
    roles = ["insurance_admin", "superuser"]
    check_role(roles, user_data['user_id'])
    admins = db.query_eng(insuranceModel.InAdmin).all()
    return admins


@router.get("/admin/insuranceID/{insuranceID}", response_model=insuranceSchema.ShowInsurance, status_code=status.HTTP_200_OK)
def show_admin(insuranceID, db: Session = Depends(load), user_data: get_current_user = Depends()):
    roles = ["insurance_admin", "superuser"]
    check_role(roles, user_data['user_id'])
    admin = db.query_eng(insuranceModel.InAdmin).filter(
        insuranceModel.InAdmin.insuranceID == insuranceID.lower()).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with the insurance ID: {insuranceID} not found")
    return admin


@router.post("/register", response_model=insuranceSchema.ShowInsurance, status_code=status.HTTP_201_CREATED)
def create_insurance(request: insuranceSchema.Insurance, db: Session = Depends(load), user_data: get_current_user = Depends()):
    roles = ["insurance_admin", "superuser"]
    check_role(roles, user_data['user_id'])
    phone = request.phone
    insuranceID = request.insuranceID.lower()
    checkPhone = db.query_eng(insuranceModel.Insurance).filter(
        insuranceModel.Insurance.phone == phone).first()
    checkInsuranceID = db.query_eng(insuranceModel.Insurance).filter(
        insuranceModel.Insurance.insuranceID == insuranceID).first()

    if checkPhone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"insurance with phone: {phone} exists")
    if checkInsuranceID:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"insurance with insurance ID: {insuranceID} exists")

    new_insurance = insuranceModel.Insurance(
        name=request.name, phone=request.phone, insuranceID=insuranceID, address=request.address)
    db.new(new_insurance)
    db.save()
    return new_insurance


@router.get("/all", response_model=List[insuranceSchema.ShowInsurance], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load), user_data: get_current_user = Depends()):
    roles = ["insurance_admin", "superuser"]
    check_role(roles, user_data['user_id'])
    companies = db.query_eng(insuranceModel.Insurance).all()
    return companies


@router.get("/{insuranceID}", response_model=insuranceSchema.ShowInsurance, status_code=status.HTTP_200_OK)
def show(insuranceID, db: Session = Depends(load), user_data: get_current_user = Depends()):
    roles = ["insurance_admin", "superuser"]
    check_role(roles, user_data['user_id'])
    company = db.query_eng(insuranceModel.Insurance).filter(
        insuranceModel.Insurance.insuranceID == insuranceID.lower()).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"company with the insurance ID: {insuranceID} not found")
    return company
