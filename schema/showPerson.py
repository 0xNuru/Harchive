from pydantic import BaseModel


class ShowPerson(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True
