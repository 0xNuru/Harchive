from pydantic import BaseModel


class Person(BaseModel):
    name: str
    email: str
    phone: str
    password: str
