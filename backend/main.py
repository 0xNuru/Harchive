from fastapi import FastAPI
import models
from database import engine
from routers import person

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(person.router)
