from fastapi import FastAPI
import models
from engine.dbStorage import DBStorage
from routers import person

get_db = DBStorage.reload()
engine = get_db.__engine

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(person.router)
