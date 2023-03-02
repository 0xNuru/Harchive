from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from schema import hospital as hospitalSchema
from engine.loadb import load
from models import hospital as hospitalModel
from sqlalchemy.orm import Session
from typing import Dict, List
from models import user as userModel
from utils import auth
from utils.oauth1 import AuthJWT
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from models import user as userModel
from sqlalchemy import or_


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
def all_admins(db: Session = Depends(load)):
    admins = db.query_eng(hospitalModel.Admin).all()
    return admins


@router.get("/admin/hospitalID/{hospitalID}", response_model=hospitalSchema.ShowHospital, status_code=status.HTTP_200_OK)
def show_admin(hospitalID, db: Session = Depends(load)):
    admin = db.query_eng(hospitalModel.Admin).filter(
        hospitalModel.Admin.hospitalID == hospitalID).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with the hospital ID: {hospitalID} not found")
    return admin


@router.post('/admin/login', status_code=status.HTTP_200_OK)
def login(response: Response, request: OAuth2PasswordRequestForm = Depends(),
          Authorize: AuthJWT = Depends(), db: Session = Depends(load)):

    user = request.username
    email = None
    password = request.password

    check = db.query_eng(hospitalModel.Admin).filter(or_(
        hospitalModel.Admin.email == email, hospitalModel.Admin.name == user)).first()

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


@router.post("/register", response_model=hospitalSchema.ShowHospital, status_code=status.HTTP_201_CREATED)
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
        name=request.name, phone=request.phone, hospitalID=request.hospitalID, address=request.address)
    db.new(new_hospital)
    db.save()
    return new_hospital


@router.get("/all", response_model=List[hospitalSchema.ShowHospital], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load)):
    hospitals = db.query_eng(hospitalModel.Hospital).all()
    return hospitals


@router.get("/{hospitalID}", response_model=hospitalSchema.ShowHospital, status_code=status.HTTP_200_OK)
def show(hospitalID, db: Session = Depends(load)):
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
def all(db: Session = Depends(load)):
    doctor = db.query_eng(hospitalModel.Doctor).all()
    return doctor


@router.get("/doctor/email/{email}", response_model=hospitalSchema.ShowDoctor, status_code=status.HTTP_200_OK)
def show(email, db: Session = Depends(load)):
    doctor = db.query_eng(hospitalModel.Doctor).filter(
        hospitalModel.Doctor.email == email).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"doctor with the email {email} not found")
    return doctor


@router.post('/doctor/login', status_code=status.HTTP_200_OK)
def login(response: Response, request: OAuth2PasswordRequestForm = Depends(),
          Authorize: AuthJWT = Depends(), db: Session = Depends(load)):

    user = request.username
    email = None
    password = request.password

    check = db.query_eng(hospitalModel.Doctor).filter(or_(
        hospitalModel.Doctor.email == email, hospitalModel.Doctor.name == user)).first()

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


@router.get('/doctor/refresh')
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


@router.get('/doctor/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.set_cookie("logged_in", '', -1)
    return {'status': 'success'}
