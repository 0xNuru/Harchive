#!/usr/bin/env python3
from fastapi import Request
from fastapi.responses import RedirectResponse
from jwt.exceptions import ExpiredSignatureError
from typing import List
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
import sys

sys.path.insert(0, '..')
from config.config import settings

class Settings(BaseModel):
    """
        Desc:
            initializes authjwt params
        Returns:
            None
    """
    authjwt_algorithm: str = settings.jwt_algorithm
    authjwt_decode_algorithms: List[str] = [settings.jwt_algorithm]

    authjwt_token_location: set = {'cookies', 'headers'}

    authjwt_access_cookie_key: str = 'access_token'

    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = False

    authjwt_secret_key: str = settings.jwt_secret_key
    


@AuthJWT.load_config
def get_config():
    """
        Desc:
            returns an instance of the
            decorated class settings
    """
    return Settings()