#!/usr/bin/python3

"""Dependencies for authenticating user"""

from typing import Any, Generator
from fastapi import Depends, HTTPException, status
from config.config import settings
from utils import auth
from utils.oauth1 import AuthJWT
from engine.loadb import load
from models import user as userModel


class NotVerified(Exception):
    pass


class UserNotFound(Exception):
    pass


def get_current_user(Authorize: AuthJWT = Depends(), db=Depends(load)):

    try:
        Authorize.jwt_required()
        user_email = Authorize.get_jwt_subject()
        data = Authorize.get_raw_jwt()
        user = db.query_eng(userModel.Users).filter(
        userModel.Users.email == user_email).first()
        if not user:
            raise UserNotFound('User no longer exist')

    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
        if error == 'UserNotFound':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='User no longer exist')
        if error == 'NotVerified':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Please verify your account')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')

    return data

