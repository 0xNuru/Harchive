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
        - __engine
        - __session
        - dic
"""

from os import getenv
from pydantic import env_settings
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
        """
        Desc:
            connects to the sql database with the params stored in env
        """
        user   = getenv("MYSQL_USER")
        passwd = getenv("MYSQL_PWD") 
        db     = getenv("MYSQL_DB")  
        host   = getenv("MYSQL_HOST") 
        connection_str = "mysql+mysqldb://{}:{}@{}/{}".format(user, passwd, host, db)
        self.__engine = create_engine(connection_str, pool_pre_ping=True)



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

    def new(self, obj):
        """
            Desc:
                adds a new object in the table
        """
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
            self.session.delete(obj)

    def reload(self):
        """
            Desc:
                 reload current connection
        """
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """ 
            Desc:
                closes the session
        """
        self.__session.close()
