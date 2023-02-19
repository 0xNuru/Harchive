from pydantic import BaseModel


class ShowHospital(BaseModel):

    name: str
    address: str

    class Config():
        orm_mode = True
