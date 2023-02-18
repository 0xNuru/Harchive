from pydantic import BaseModel


class ShowPatient(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True
