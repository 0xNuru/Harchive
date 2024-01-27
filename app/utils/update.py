#!/usr/bin/env python

import datetime
import multiprocessing
from engine.loadb import load
from models import user as userModel

# cache implementation to store user tokens mapped to emails
# from cachetools import TTLCache


# class JSONCache:
#     def __init__(self, maxsize=100, ttl=300):
#         self.cache = TTLCache(maxsize=maxsize, ttl=ttl)

#     def get(self, key):
#         return self.cache.get(key)

#     def set(self, key, value):
#         self.cache[key] = value

#     def delete(self, key):
#         if key in self.cache:
#             del self.cache[key]

# # Create an instance of JSONCache
# json_cache = JSONCache()


def run_function_async(target_function, *args, **kwargs):

    # Create a new process
    process = multiprocessing.Process(
        target=target_function, args=args, kwargs=kwargs)
    process.start()

    return


def get_min(dattime):
    result = datetime.datetime.now() - dattime
    seconds = int(result.total_seconds())

    return seconds


def update_db():
    # initialize database
    db_gen = load()
    db = next(db_gen)

    users = db.query_eng(userModel.Users).filter(
        userModel.Users.is_verified == False).all()

    # delte all users who's verification is timed out
    for user in users:
        if get_min(user.created_at) >= 300:
            db.delete(user)
            db.save()


def clean_db():

    run_function_async(update_db)

    return
