from fastapi import APIRouter, Depends, status
# from schema*
from schema import person, showPerson
# from models*
from engine.dbStorage import DBStorage
from models import person
from sqlalchemy.orm import Session


router = APIRouter(
    tags=["person"]
)
get_db = DBStorage.reload()


@router.post("/person", response_model=showPerson, status_code=status.HTTP_201_CREATED)
def create_person(request: person.Person, db: Session = Depends(get_db)):
    new_person = person(name=request.name, email=request.email,
                        phone=request.phone, password=request.password)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person
