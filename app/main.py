#!/usr/bin/python3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, insurance, hospital, patient
import sys

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
