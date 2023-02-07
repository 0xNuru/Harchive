from pydantic import BaseModel


class Person(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    password: str


class ShowPerson(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True
