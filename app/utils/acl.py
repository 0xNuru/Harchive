#!/usr/bin/python3


"""Searches for a user and return claims"""

from typing import List
from engine.loadb import load
from fastapi import HTTPException
import models as userModel
from models import patient
from models import hospital
from models import insurance
from sqlalchemy.orm import Session
from starlette import status


def check_role(roles: List[str], user_id: str) -> None:
    """
        Doc:
            searches for users perms,
        Return:
            returns None if succed
    """
    model = {'patient': ['patient', 'Patient'], 'insurance_admin': ['insurance', 'InAdmin'],
             'hospital_admin': ['hospital', 'Admin'], 'doctor': ['hospital', 'Doctors'], 'superuser':['user', 'Superuser']}

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


def create_perms(role: str):
    pass
