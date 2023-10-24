#!/usr/bin/python3


"""Searches for a user and return claims"""

from datetime import datetime
from typing import List
from engine.loadb import load
from fastapi import HTTPException
import models as userModel
from models import patient
from models import hospital
from models import insurance
from pydantic import EmailStr
from starlette import status


def check_role(roles: List[str], user_id: str) -> None:
    """
        Doc:
            searches for users perms,
        Return:
            returns None if succed
    """
    model = {'patient': ['patient', 'Patient'], 'insurance_admin': ['insurance', 'InAdmin'],
             'hospital_admin': ['hospital', 'Admin'], 'doctor': ['hospital', 'Doctors'], 'superuser':['user', 'Users']}

    db_gen = load()
    db = next(db_gen)
    for role in roles:
        inst = getattr(userModel, model[role][0])

        user = getattr(inst, model[role][1])

        search = db.query_eng(user).filter(
            user.id == user_id).first()

        if search:
            return None

    if not search:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Permission denied")

    if search.role != role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Permission denied')

from pydantic import BaseModel, EmailStr
def create_perms(role: str):
    pass


# implementing the jail features

# updates the user field
def change_user_state(email: EmailStr,
                      suspended_at =None,
                      suspend: bool=None):
    
    db_gen = load()
    db = next(db_gen)

    user = db.query_eng(userModel.Users).filter(
        userModel.Users.email == email).first()

    # Update columns based on suspend value

    if suspend:
        user.is_suspended = True
        user.suspended_at = suspended_at
    else:
         user.is_suspended = False

    db.update(user)
    db.save()

def update_max_trys(email: EmailStr, tryalls: int) -> None:

    db_gen = load()
    db = next(db_gen)

    user = db.query_eng(userModel.Users).filter(
        userModel.Users.email == email).first()

    if user.failed_login_attempts == None:
        user.failed_login_attempts = 0

    # Increment the failed login attempts

    user.failed_login_attempts += 1
    db.update(user)
    db.save()

    # Check if the count exceeds tryalls
    if user.failed_login_attempts >= tryalls:
        # If it does, suspend the user and set suspended_at to the current datetime
        suspend_time = datetime.utcnow()
        change_user_state(email, suspend_time, True)

def reset_user_state(email: EmailStr) -> None:

    db_gen = load()
    db = next(db_gen)

    user = db.query_eng(userModel.Users).filter(
        userModel.Users.email == email).first()

    # reset the failed login attempts
    user.failed_login_attempts = 0

    # unsuspend the user
    change_user_state(email, suspended_at=None, suspend=False)
    db.update(user)
    db.save()

