#!/usr/bin/python3

"""
Class for sqlAlchemy that handles session connections

contains:
    - instance:
        - all
        - new
        - save
        - delete
        - reload
        - close

    - attributes:
        - __engine
        - __session
        - dic
"""

from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base


class DBStorage:
    """
    Desc:
        Creates tables in the database
    """
    __engine = None
    __session = None

    def __init__(self):
        user
        passwd
        db
        host
 


        connection_str = "mysql+mysqldb://{}:{}@{}/{}".format(user, passwd, host, db)
        __engine = sqlalchemy.create_engine(connection_str, pool_pre_ping=True)