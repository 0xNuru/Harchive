#!/usr/bin/python3

"""
A setup script for setting mysql server details to current working envionment
all details inputed are set to the environment variables

"""

import os
import sqlalchemy


user     =  input("ENTER THE SQL USERNAME : ")
passwd   =  input("ENTER THE MYSQL PASSWORD :")
db   =  input("ENTER THE MYSQL Database Name :")
host =  input("ENTER THE MYSQL HOST NAME :")

connection_str = "mysql+mysqldb://{}:{}@{}/{}".format(user, passwd, host, db)
engine = sqlalchemy.create_engine(connection_str, pool_pre_ping=True)


try:
    conn = engine.connect()
    conn.close()

    os.environ["MYSQL_USER"]  = user
    os.environ["MYSQL_PWD"]   = passwd
    os.environ["MYSQL_DB"]    = db
    os.environ["MYSQL_HOST"]  = host

    print("mysql connected successfully !!")

except Exception as e:
    print(f"This {e} occured !!! ")
