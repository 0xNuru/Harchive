from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    password: str
