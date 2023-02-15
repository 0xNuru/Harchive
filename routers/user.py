from fastapi import APIRouter, Depends, status
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
    new_user = userModel.Users(name=request.name, email=request.email,
                               phone=request.phone, password=request.password)
    db.new(new_user)
    db.save()
    db.refresh(new_user)
    return new_user
