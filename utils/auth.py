#!/usr/bin/env python3
from datetime import datetime, timedelta, timezone
from typing import Any
from utils.oauth1 import AuthJWT
from fastapi import Response
from passlib.context import CryptContext
from config.config import settings


# Password hash context

auth = AuthJWT()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRES_IN = settings.token_life_span * 60
REFRESH_TOKEN_EXPIRES_IN = settings.token_long_life_span * 60

def verify_password(plain_password: str, hashed_password: str) -> bool:
    verified: bool = pwd_context.verify(plain_password, hashed_password)
    return verified


def get_password_hash(password: str) -> str:
    hash: str = pwd_context.hash(password)
    return hash



def set_access_cookies(token: str,response: Response):
    response.set_cookie(
        key='access_token',
        value=token,
        max_age=ACCESS_TOKEN_EXPIRES_IN * 60,
        expires=ACCESS_TOKEN_EXPIRES_IN * 60,
        path='/',
        domain=None,
        secure=False,
        httponly=True,
        samesite='lax'
    )


def set_refresh_cookies(token: str,response: Response):
    response.set_cookie(
        key='refresh_token',
        value=token,
        max_age=REFRESH_TOKEN_EXPIRES_IN * 60,
        expires=REFRESH_TOKEN_EXPIRES_IN * 60,
        path='/',
        domain=None,
        secure=False,
        httponly=True,
        samesite='lax'
    )


def access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
    access_token : str = auth.create_access_token(subject=
        to_encode['email'], 
        expires_time = expire,
        user_claims = to_encode
    )
    return access_token

def refresh_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire =  timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN)
    refresh_token : str = auth.create_refresh_token(subject=
        to_encode['email'], 
        expires_time = expire,
        user_claims = to_encode
    )
    return refresh_token

