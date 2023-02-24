#!/usr/bin/python

""" sets environment variable using pydantic BaseSettings"""

from typing import Any
from pydantic import BaseSettings, validator
from enum import Enum
import sys

class Envtype(str, Enum):
    local: str = "Development"


class Settings(BaseSettings):
    """
        Desc:
            contains all required settings
    """
    proj_name : str = ""

    # database settings

    dbUSER : str
    dbPWD  : str
    dbDB   : str
    dbHOST : str
    DATABASE_URL : str

    # jwt settings
    jwt_secret_key: str
    jwt_algorithm: str
    token_life_span: int
    token_long_life_span: int
    tokenUrl: str

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        
settings = Settings()


