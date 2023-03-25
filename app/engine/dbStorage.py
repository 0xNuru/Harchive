#!/usr/bin/python3

"""
Class for sqlAlchemy that handles __session connections

contains:
    - instance:
        - all: query objects from db
        - new: add objects to db
        - save: commit __session
        - delete: remove __session from db
        - reload: reload the current __session
        - close: end __session

    - attributes:
        - engine
        - __session
        - dic
"""
from google.cloud.sql.connector import Connector, IPTypes
from config.config import settings
from models.base_model import Base, BaseModel
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from pydantic import env_settings
from dotenv import load_dotenv
import psycopg2
import os
from os import getenv
import sys
sys.path.insert(0, '..')

load_dotenv()

connector = Connector()


def login():
    user = input("ENTER THE SQL USERNAME : ")
    passwd = input("ENTER THE MYSQL PASSWORD :")
    db = input("ENTER THE MYSQL Database Name :")
    host = input("ENTER THE MYSQL HOST NAME :")

    connection_str = "postgresql+psycopg2://{}:{}@{}/{}".format(
        user, passwd, host, db)
    engine = create_engine(connection_str, pool_pre_ping=True)

    try:
        conn = engine.connect()
        conn.close()

        os.environ["dbUSER"] = user
        os.environ["dbPWD"] = passwd
        os.environ["dbDB"] = db
        os.environ["dbHOST"] = host

        # psql
        print("mysql connected successfully !!")

    except Exception as e:

        print(f"This {e} occured !!! ")


if not os.getenv("dbUSER"):
    login()


def getconn():
    conn = connector.connect(
            settings.dbHost_instance ,
            "pg8000",
            user=settings.dbUSER,
            password=settings.dbPWD,
            db=settings.dbDB,
            ip_type=IPTypes.PUBLIC
        )
    return conn


class DBStorage:
    """
    Desc:
        Creates tables in the database
    """
    engine = None
    __session = None

    def __init__(self):
        """
        Desc:
            connects to the sql database with the params stored in env
        """

        # user = getenv("dbUSER")
        # passwd = getenv("dbPWD")
        # db = getenv("dbDB")
        # host = getenv("dbHost_instance")
        # connection_str = "postgresql+psycopg2://{}:{}@{}/{}".format(
        #     user, passwd, host, db)
        # self.engine = create_engine(connection_str, pool_pre_ping=True)

        SQLALCHEMY_DATABASE_URL = "postgresql+pg8000://"

        self.engine = create_engine(SQLALCHEMY_DATABASE_URL, creator=getconn,
            pool_pre_ping=True)

        self.__session = None

    def all(self, cls=None):
        """ 
            Desc:
                returns a dictionary of all objects(tables)
                in the database
            Return:
                returns a dictionary of __object
        """
        dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                dic[key] = elem
        else:
            lists = []
            for attr in lists:
                query = self.__session.query(attr)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    dic[key] = elem
        return (dic)

    def query_eng(self, cls=None):
        """
            Desc:
                returns query object
        """
        return self.__session.query(cls)

    def new(self, obj):
        """
            Desc:
                adds a new object in the table
        """
        print(self.__session)
        self.__session.add(obj)

    def save(self):
        """
            Desc:
                commit changes
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
            Desc:
                delete an element from the table
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
            Desc:
                 reload current connection
        """
        Base.metadata.create_all(self.engine)
        sec = sessionmaker(bind=self.engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """ 
            Desc:
                closes the __session
        """
        self.__session.close()
