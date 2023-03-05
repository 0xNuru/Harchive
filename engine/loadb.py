#!/usr/bin/python3

"""Initializes the storage engine"""

import sys
sys.path.insert(0, '..')
from engine.dbStorage import DBStorage


def load():
    """
        Desc:
            initialize the db
    """

    get_db = DBStorage()
    get_db.reload()
    try:
        yield get_db

    finally:
        get_db.close()
