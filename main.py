from fastapi import FastAPI
import models.base_model 
from engine.dbStorage import DBStorage
from routers import user
import sys

sys.path.insert(0, '..')

get_db = DBStorage()
get_db.reload()

engine = get_db.engine

app = FastAPI()

models.base_model.Base.metadata.create_all(engine)

app.include_router(user.router)
