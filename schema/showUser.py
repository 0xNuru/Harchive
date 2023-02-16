from pydantic import BaseModel


class ShowUser(BaseModel):
    
    name: str
    email: str

    class Config():
        orm_mode = True
