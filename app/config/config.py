#!/usr/bin/python

""" sets environment variable using pydantic BaseSettings"""

from typing import Any
from dotenv import load_dotenv
from pydantic import BaseSettings, validator, EmailStr
from enum import Enum
import sys
sys.path.insert(0, '../')

load_dotenv()
class Envtype(str, Enum):
    local: str = "Development"


class Settings(BaseSettings):
    """
        Desc:
            contains all required settings
    """
    proj_name : str = ""

    #  database settings
    dbUSER : str
    dbPWD  : str
    dbDB   : str
    dbHost_instance : str
    DATABASE_URL : str

    # jwt settings
    jwt_secret_key: str
    jwt_algorithm: str
    token_life_span: int
    token_long_life_span: int
    tokenUrl: str

    #  email settings
    EMAIL_HOST: str
    EMAIL_PORT: str
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: EmailStr

    #  google authentication settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    secret_key: str
    

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        
settings = Settings()
