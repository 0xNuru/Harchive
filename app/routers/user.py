#!/usr/bin/python3

""" User logging endpoint"""


from utils.logger import logger
from utils.oauth1 import AuthJWT
from utils import auth
from typing import List
from starlette import status
from sqlalchemy.orm import Session
from schema import user as userSchema
from models import user as userModel
from models import patient as patientModel
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from engine.loadb import load
from dependencies.depends import get_current_user
import sys
from utils.email import Email, generateToken, verifyToken
from jinja2 import Environment, select_autoescape, PackageLoader
from utils.auth import oauth, OAuthError
from utils import acl, utime
from utils.email import verifyEmail

sys.path.insert(0, '..')

router = APIRouter(
    prefix='/user',
    tags=["user"]
)


env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

@router.post("/register", response_model=userSchema.ShowUser,
             status_code=status.HTTP_201_CREATED)
async def create_user(request: userSchema.User, http_request: Request, db: Session = Depends(load)):
    phone = request.phone
    email = request.email

    checkPhone = db.query_eng(userModel.Users).filter(
        userModel.Users.phone == phone).first()
    checkEmail = db.query_eng(userModel.Users).filter(
        userModel.Users.email == email).first()
    if checkPhone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=[{"msg":f"user with phone: {phone} exists"}])
    if checkEmail:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=[{"msg":f"user with email: {email} exists"}])
    
    await verifyEmail(email, http_request, request)
    
    del request.password1
    passwd_hash = auth.get_password_hash(request.password2.get_secret_value())


    new_user = userModel.Users(name=request.name, phone=request.phone,
                               email=request.email, address=request.address,
                               password_hash=passwd_hash, role="superuser", is_verified=False)
    logger.info(f"user with the name {request.name} has been created")
    db.new(new_user)
    db.save()


    return {"name": request.name, "email": email, "role": new_user.role, "message": "Verification\
            email sent successfully"}



# protected route that requires login, uses the get_current_user func
@router.get("/all", response_model=List[userSchema.ShowUser], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load), user_data: get_current_user = Depends()):
    users = db.query_eng(userModel.Users).all()
    logger.info(f"user with the email {user_data['email']}  queried all users")
    return users


@router.get("/email/{email}", response_model=userSchema.ShowUser, status_code=status.HTTP_200_OK)
def show(email, db: Session = Depends(load)):
    users = db.query_eng(userModel.Users).filter(
        userModel.Users.email == email).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=[{"msg":f"user with the email {email} not found"}])
    return users

