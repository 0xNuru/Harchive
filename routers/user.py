from fastapi import APIRouter, Depends, status
from schema import User, showUser
from engine.dbStorage import DBStorage
from models import user
from sqlalchemy.orm import Session
from typing import Dict, List

router = APIRouter(
    tags=["user"]
)
get_db = DBStorage()
get_db.reload()



@router.post("/user", response_model=showUser.ShowUser,
 status_code=status.HTTP_201_CREATED)
def create_user(request: User.User, db: Session = Depends(DBStorage)):
    new_user = user(name=request.name, email=request.email,
                        phone=request.phone, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
