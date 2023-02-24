from fastapi import FastAPI
import models.base_model
from fastapi.middleware.cors import CORSMiddleware
from engine.dbStorage import DBStorage
from routers import user, insurance, hospital, patient
import sys

# sys.path.insert(0, '..')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(insurance.router)
app.include_router(hospital.router)
app.include_router(patient.router)
