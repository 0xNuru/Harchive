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


def test_login_user():
    """_summary_
    """

    resopnse = client.post("/user/login")
    
    assert resopnse.status_code == 200



def test_user_logout():
    """_summary_
    """

    response = client.get("/user/logout")

    assert response.status_code == 200