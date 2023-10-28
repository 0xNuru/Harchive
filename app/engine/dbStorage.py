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
from os import getenv
import os
import psycopg2
from dotenv import load_dotenv
from pydantic import env_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
from config.config import settings
from google.cloud.sql.connector import Connector, IPTypes
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
        os.environ["dbHost_instance"] = host

        # psql
        print("mysql connected successfully !!")

    except Exception as e:

        print(f"This {e} occured !!! ")


if not os.getenv("dbUSER"):
    login()


def getconn():
    conn = connector.connect(
        settings.dbHost_instance,
        "pg8000",
        user=settings.dbUSER,
        password=settings.dbPWD,
        db=settings.dbDB,
        ip_type=IPTypes.PUBLIC
    )
    return conn


def is_postgresql_up(db_url):
    """_summary_: checks if postgresql is available

    Args:
        db_url (str): database url
    """
    try:
        # Attempt to create an SQLAlchemy engine and connect to the database
        engine = create_engine(db_url)
        connection = engine.connect()
        connection.close()
        return True

    except Exception:
        return False
        


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

        user = getenv("dbUSER")
        passwd = getenv("dbPWD")
        db = getenv("dbDB")
        host = getenv("dbHost_instance")
        connection_str = "postgresql+psycopg2://{}:{}@{}/{}".format(
             user, passwd, host, db)

        if is_postgresql_up(connection_str):
            self.engine = create_engine(connection_str, pool_pre_ping=True)
        else:
            print("PostgreSQL is not running or the connection failed.")

        # SQLALCHEMY_DATABASE_URL = "postgresql+pg8000://"

        # self.engine = create_engine(SQLALCHEMY_DATABASE_URL, creator=getconn,
        #                             pool_pre_ping=True)

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
        self.__session.add(obj)

    def update(self, obj):
        """
        Desc:
            Update an existing object in the database.
        Args:
            obj: The object to update.
        """
        try:
            self.__session.merge(obj)
        except Exception as e:
            print("Error updating object:", str(e))
            self.__session.rollback()

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
