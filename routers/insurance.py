from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from schema import insurance as insuranceSchema
from engine.loadb import load
from models import inusrance as insuranceModel
from sqlalchemy.orm import Session
from typing import Dict, List
from utils import auth
from utils.oauth1 import AuthJWT
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from models import user as userModel
from sqlalchemy import or_


from utils import auth

router = APIRouter(
    prefix="/insurance",
    tags=["insurance"]
)


@router.post("/admin/register", response_model=insuranceSchema.ShowInsurance, status_code=status.HTTP_201_CREATED)
def create_in_admin(request: insuranceSchema.InAdmin, db: Session = Depends(load)):
    phone = request.phone
    insuranceID = request.insuranceID

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

    passwd_hash = auth.get_password_hash(request.password2.get_secret_value())

    new_inAdmin = insuranceModel.InAdmin(
        name=request.name, phone=request.phone, email=request.email, password_hash=passwd_hash, insuranceID=request.insuranceID)
    db.new(new_inAdmin)
    db.save()
    return new_inAdmin


@router.get("/admin/all", response_model=List[insuranceSchema.ShowInsurance], status_code=status.HTTP_200_OK)
def all_admins(db: Session = Depends(load)):
    admins = db.query_eng(insuranceModel.InAdmin).all()
    return admins


@router.get("/admin/insuranceID/{insuranceID}", response_model=insuranceSchema.ShowInsurance, status_code=status.HTTP_200_OK)
def show_admin(insuranceID, db: Session = Depends(load)):
    admin = db.query_eng(insuranceModel.InAdmin).filter(
        insuranceModel.InAdmin.insuranceID == insuranceID).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with the insurance ID: {insuranceID} not found")
    return admin


@router.post("/register", response_model=insuranceSchema.ShowInsurance, status_code=status.HTTP_201_CREATED)
def create_insurance(request: insuranceSchema.Insurance, db: Session = Depends(load)):
    phone = request.phone
    insuranceID = request.insuranceID

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
        name=request.name, phone=request.phone, insuranceID=request.insuranceID, address=request.address)
    db.new(new_insurance)
    db.save()
    return new_insurance


@router.get("/all", response_model=List[insuranceSchema.ShowInsurance], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load)):
    companies = db.query_eng(insuranceModel.Insurance).all()
    return companies


@router.get("/{insuranceID}", response_model=insuranceSchema.ShowInsurance, status_code=status.HTTP_200_OK)
def show(insuranceID, db: Session = Depends(load)):
    company = db.query_eng(insuranceModel.Insurance).filter(
        insuranceModel.Insurance.insuranceID == insuranceID).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"company with the insurance ID: {insuranceID} not found")
    return company


@router.post('/admin/login', status_code=status.HTTP_200_OK)
def login(response: Response, request: OAuth2PasswordRequestForm = Depends(),
          Authorize: AuthJWT = Depends(), db: Session = Depends(load)):

    user = request.username
    email = None
    password = request.password

    check = db.query_eng(insuranceModel.InAdmin).filter(or_(
        insuranceModel.InAdmin.email == email, insuranceModel.InAdmin.name == user)).first()

    if not check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Incorrect Username or Password")

    if not auth.verify_password(password, check.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Username or Password')

    data = {
        'username': check.name,
        'email': check.email,

    }

    # generate user cookies
    access_token = auth.access_token(data)
    refresh_token = auth.refresh_token(data)

    # save tokens in the cookies
    auth.set_access_cookies(access_token, response)
    auth.set_refresh_cookies(refresh_token, response)

    return {"msg": "user logged in"}


@router.get('/admin/refresh')
async def refresh(request: Request, response: Response, Authorize: AuthJWT = Depends(), db: Session = Depends(load)):

    try:

        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')

        check = db.query_eng(userModel.Users).filter(
            userModel.Users.name == user_id).first()

        if not check:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            redirect_url = request.url_for('login')
            return JSONResponse(content={"redirect_url": redirect_url, "redirect": True}, status_code=307)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    data = {
        'username': check.name,
        'email': check.email,

    }

    # generate user cookies
    access_token = auth.access_token(data)

    # save tokens in the cookies
    auth.set_access_cookies(access_token, response)

    return {"msg": "access token refreshed", 'user_id': user_id}


@router.get('/admin/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.set_cookie("logged_in", '', -1)
    return {'status': 'success'}
