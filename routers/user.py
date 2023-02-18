from fastapi import APIRouter, Depends, status, HTTPException
from schema import showUser
from schema import user as userSchema
from engine.loadb import load
from models import user as userModel
from sqlalchemy.orm import Session
from typing import Dict, List

router = APIRouter(
    tags=["user"]
)


@router.post("/user", response_model=showUser.ShowUser,
             status_code=status.HTTP_201_CREATED)
def create_user(request: userSchema.User, db: Session = Depends(load)):
    phone = request.phone
    email = request.email

    checkPhone = db.query_eng(userModel.Users).filter(
        userModel.Users.phone == phone).first()
    checkEmail = db.query_eng(userModel.Users).filter(
        userModel.Users.email == phone).first()
    if checkPhone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"user with phone: {phone} exists")
    if checkEmail:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"user with email: {email} exists")

    new_user = userModel.Users(name=request.name, phone=request.phone,
                               email=request.email, address=request.address, password=request.password)
    db.new(new_user)
    db.save()
    return new_user


@router.get("/users", response_model=List[showUser.ShowUser], status_code=status.HTTP_200_OK)
def all(db: Session = Depends(load)):
    users = db.query_eng(userModel.Users).all()
    return users


@router.get("/user/{email}", response_model=showUser.ShowUser, status_code=status.HTTP_200_OK)
def show(email, db: Session = Depends(load)):
    users = db.query_eng(userModel.Users).filter(
        userModel.Users.email == email).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with the email {email} not found")
    return users
