#!/usr/bin/python3

from fastapi import APIRouter, Depends, status, HTTPException, Response
from schema import showUser
from fastapi.security import OAuth2PasswordRequestForm
from schema import user as userSchema
from engine.loadb import load
from sqlalchemy import or_
from models import user as userModel
from utils import auth
from utils.oauth1 import AuthJWT
from sqlalchemy.orm import Session
from typing import Dict, List
from dependencies.depends import get_current_user



router = APIRouter(
    prefix='/user',
    tags=["user"]
)


@router.post("/register", response_model=showUser.ShowUser,
             status_code=status.HTTP_201_CREATED)
def create_user(request: userSchema.User, db: Session = Depends(load)):
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

    new_user = userModel.Users(name=request.name, phone=request.phone,
                               email=request.email, address=request.address, 
                               password_hash=passwd_hash)
    db.new(new_user)
    db.save()
    return new_user


@router.get("/all", response_model=List[showUser.ShowUser], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load)):
    users = db.query_eng(userModel.Users).all()
    return users



@router.get("/email/{email}", response_model=showUser.ShowUser, status_code=status.HTTP_200_OK)
def show(email, db: Session = Depends(load)):
    users = db.query_eng(userModel.Users).filter(
        userModel.Users.email == email).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with the email {email} not found")
    return users


# logging endpoint 

@router.post('/login', status_code=status.HTTP_200_OK)
def login(response: Response, request: OAuth2PasswordRequestForm = Depends(),
     Authorize: AuthJWT = Depends(), db: Session = Depends(load)):

    user = request.username
    email = None
    password = request.password

    check = db.query_eng(userModel.Users).filter(or_(
        userModel.Users.email == email, userModel.Users.name == user)).first()


    if not check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Incorrect Username and Password")
    
    if not auth.verify_password(password, check.password_hash):
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Username and Password')
    
    data = {
        'username': check.name,
        'email' : check.email,
        
    }
    
    # generate user cookies
    access_token = auth.access_token(data)
    refresh_token = auth.refresh_token(data)

    # save tokens in the cookies
    auth.set_access_cookies(access_token, response)
    auth.set_refresh_cookies(refresh_token, response)

    return {"msg": "user logged in"}


@router.get('/refresh')
def refresh(response: Response, Authorize: AuthJWT = Depends(), db: Session = Depends(load)):

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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    
    data = {
        'username': check.name,
        'email' : check.email,
        
    }
    
    # generate user cookies
    access_token = auth.access_token(data)

    # save tokens in the cookies
    auth.set_access_cookies(access_token, resp)

    return {"msg": "access token refreshed"}

@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    print(Authorize.get_raw_jwt())
    return {'status': 'success'}