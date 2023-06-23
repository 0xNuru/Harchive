#!/usr/bin/python3

from routers import user, insurance, hospital, patient
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import sys
sys.path.insert(0, '..')


# sys.path.insert(0, '..')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(insurance.router)
app.include_router(hospital.router)
app.include_router(patient.router)
