from person import Person


class HealthWorker(Person):
    hospitalID: str

    class Config():
        orm_mode = True
