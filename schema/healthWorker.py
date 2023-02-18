from user import User


class HealthWorker(User):
    hospitalID: str

    class Config():
        orm_mode = True
