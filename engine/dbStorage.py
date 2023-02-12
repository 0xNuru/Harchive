#!/usr/bin/python3

"""
Class for sqlAlchemy that handles session connections

contains:
    - instance:
        - all: query objects from db
        - new: add objects to db
        - save: commit session
        - delete: remove session from db
        - reload: reload the current session
        - close: end session

    - attributes:
        - engine
        - session
        - dic
"""
import sys
sys.path.insert(0, '..')

from models.base_model import Base
from os import getenv
import os
import psycopg2
from dotenv import load_dotenv
from pydantic import env_settings
from sqlalchemy.orm import sessionmaker, scoped_session 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()


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

        print("mysql connected successfully !!")

    except Exception as e:

        print(f"This {e} occured !!! ")




if  not os.getenv("dbUSER"):
    login()

class DBStorage:
    """
    Desc:
        Creates tables in the database
    """
    engine = None
    session = None

    def __init__(self):
        """
        Desc:
            connects to the sql database with the params stored in env
        """

        user   = getenv("dbUSER")
        passwd = getenv("dbPWD") 
        db     = getenv("dbDB")  
        host   = getenv("dbHOST") 
        connection_str = "postgresql+psycopg2://{}:{}@{}/{}".format(user, passwd, host, db)
        self.engine = create_engine(connection_str, pool_pre_ping=True)


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
            query = self.session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                dic[key] = elem
        else:
            lists = []
            for attr in lists:
                query = self.session.query(attr)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    dic[key] = elem
        return (dic)

    def new(self, obj):
        """
            Desc:
                adds a new object in the table
        """
        self.session.add(obj)

    def save(self):
        """
            Desc:
                commit changes
        """
        self.session.commit()

    def delete(self, obj=None):
        """
            Desc:
                delete an element from the table
        """
        if obj:
            self.session.delete(obj)

    def reload(self):
        """
            Desc:
                 reload current connection
        """
        Base.metadata.create_all(self.engine)
        sec = sessionmaker(bind=self.engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.session = Session()

    def close(self):
        """ 
            Desc:
                closes the session
        """
        self.session.close()

p = DBStorage()
print(p.reload())