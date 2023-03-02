from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from schema import patient as patientSchema
from engine.loadb import load
from models import user as userModel
from models import patient as patientModel
from sqlalchemy.orm import Session
from typing import Dict, List
from utils import auth
from utils.oauth1 import AuthJWT
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from models import user as userModel
from sqlalchemy import or_


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


@router.get("/all", response_model=List[patientSchema.ShowPatient], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load)):
    patient = db.query_eng(patientModel.Patient).all()
    return patient


@router.get("/email/{email}", response_model=patientSchema.ShowPatient, status_code=status.HTTP_200_OK)
def show(email, db: Session = Depends(load)):
    patient = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.email == email).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with the email {email} not found")
    return patient


@router.post('/login', status_code=status.HTTP_200_OK)
def login(response: Response, request: OAuth2PasswordRequestForm = Depends(),
          Authorize: AuthJWT = Depends(), db: Session = Depends(load)):

    user = request.username
    email = None
    password = request.password

    check = db.query_eng(patientModel.Patient).filter(or_(
        patientModel.Patient.email == email, patientModel.Patient.name == user)).first()

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


@router.get('/refresh')
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


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.set_cookie("logged_in", '', -1)
    return {'status': 'success'}
