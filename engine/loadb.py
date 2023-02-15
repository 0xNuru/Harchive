#!/usr/bin/python3

"""Initializes the storage engine"""

from engine.dbStorage import DBStorage


def load():
    """
        Desc:
            initialize the db
    """
    
    get_db = DBStorage()
    get_db.reload()
    yield get_db
