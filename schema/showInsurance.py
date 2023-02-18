from pydantic import BaseModel


class ShowInsurance(BaseModel):

    name: str
    address: str

    class Config():
        orm_mode = True
