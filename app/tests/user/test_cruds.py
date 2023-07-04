#!/usr/bin/python3
'''
Desc: Writing tests for the Models
'''
import sys
sys.path.insert(0, '../..')
from main import app
from pydantic import BaseModel
from fastapi.testclient import TestClient
from typing import Any
from pydantic import EmailStr

client = TestClient(app)


# User test Cases

def test_user_created():
    """
        Desc: Test creation of users
    """
    response = client.post("/user/register", 
                           json={
                                "name": "FastAPi_Test3",
                                "email": "FAST3@example.com",
                                "phone": "+213371337133",
                                "address": "@FastStreet 123",
                                "password1": "Staff@fas7t3k",
                                "password2": "Staff@fas7t3k",
                                },
                            )
    assert response.status_code == 201 or response.status_code == 409 ## the or statement is in effect if test cas is runned
                                                                      ## for the second time


def test_getAll_users():
    """
        Desc: Returns a list of users in database
        Return: list of users
    """
    response = client.get("/user/all")
    
    assert response.status_code == 200 or response.status_code == 401


def test_get_user_email():
    """_summary_
    """
    email = 'FAST3@example.com'
    response = client.get(f"/user/email/{email}")

    assert response.status_code == 200
    
    assert response.json() == {
                                "name": "FastAPi_Test3",
                                "email": f"{email}",
                            }


def test_refresh_user():
    """_summary_
    """

    response = client.get("/user/refresh")

    assert response.status_code == 307



## Patient Test cases

def test_patient_register():
    """_summary_
    """

    body = {
                "name": "string",
                "nin": "stringstrin",
                "email": "user@example.com",
                "password1": "Staff@fas7t3k",
                "password2": "Staff@fas7t3k",
                "gender": "M",
                "dob": "2023-07-01",
                "phone": "stringstrin",
                "address": "stringstri",
                "insuranceID": "string"
            }
    
    response = client.post("/patient/register", json=body)

    assert response.status_code == 201  or response.status_code == 409

    # assert response.json() == { "name": "string",
    #                             "email": "user@example.com",
    #                             "nin": "stringstrin",
    #                         }



def test_all_patient():
    """_summary_
    """

    response = client.get("/patient/all")

    assert response.status_code == 200 or response.status_code == 401



def test_get_patient_email():
    """_summary_
    """
    email = 'user@example.com'
    response = client.get(f"/patient/email/{email}")

    assert response.status_code == 200 or response.status_code == 401


def test_patient_record_add():
    """_summary_
    """

    body = {
            "type": "string",
            "DOB": "2023-07-01",
            "BloodType": "strin",
            "Height": 0,
            "weight": 0,
            "BMI": 0,
        }
    
    response = client.post("/patient/record/add", json=body)

    assert response.status_code == 201 or response.status_code == 401


def test_patient_record_all():
    """_summary_
    """

    body = {
            "type": "string",
            "DOB": "2023-07-01",
            "BloodType": "strin",
            "Height": 0,
            "weight": 0,
            "BMI": 0,
        }
    
    response = client.get("/patient/record/all")

    assert response.status_code == 200  or response.status_code == 401

    # assert response.json()[0] == body


def test_patient_record_nin():
    """_summary_
    """

    nin = 'stringstrin'

    body = {
            "type": "string",
            "DOB": "2023-07-01",
            "BloodType": "strin",
            "Height": 0,
            "weight": 0,
            "BMI": 0,
        }

    response = client.get(f"/patient/record/nin/{nin}")

    assert response.status_code == 200  or response.status_code == 401

    # assert response.json() == body



def test_patient_record_update():
    """_summary_
    """

    nin = 'stringstrin'
    
    body = {
            "type": "stringsss",
            "DOB": "2023-07-01",
            "BloodType": "strin",
            "Height": 0,
            "weight": 0,
            "BMI": 0,
        }
    
    response = client.put(f"/patient/record/update/{nin}", json=body)
    
    assert response.status_code == 200  or response.status_code == 401

    # assert response.json() == body


def test_patient_medcation_add():
    """_summary_
    """

    nin = 'stringstrin'

    body = {
            "medication_name": "string",
            "dosage": "string",
            "start_date": "2023-07-01",
            "due_date": "2023-07-01",
            "reason": "string"
        }
    
    response = client.post(f"/patient/medication/add/{nin}", json=body)
    
    assert response.status_code == 201  or response.status_code == 401

    # assert response.json() == body


def test_patient_allergy_add():
    z"""_summary_
    """

    nin = 'stringstrin'

    body = {
            "allergy_name": "string",
            "type": "FOOD",
            "reactions": "string",
            "more_info": "string"
        }
    
    response = client.post(f"/patient/allergy/add/{nin}", json=body)
    
    assert response.status_code == 201  or response.status_code == 401

    # assert response.json() == body



def test_patient_immunization_add():
    """_summary_
    """

    nin = 'stringstrin'

    body = {
            "name": "string",
            "immunization_date": "2023-07-01",
            "immunization_location": "string",
            "lot_number": "string",
            "expiry_date": "2023-07-01",
            "more_info": "string",
            "doctor_name": "string"
        }
    
    response = client.post(f"/patient/immunization/add/{nin}", json=body)
    
    assert response.status_code == 201  or response.status_code == 401

    # assert response.json() == body


def test_patient_transaction_add():
    """_summary_
    """

    nin = 'stringstrin'

    body = {
            "description": "string",
            "quantity": 0
            }
    
    response = client.post(f"/patient/transaction/add/{nin}", json=body)
    
    assert response.status_code == 201  or response.status_code == 401

    # assert response.json() == body


    
    