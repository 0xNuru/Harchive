from fastapi import APIRouter, Depends, status
import schema
import database
import models
from sqlalchemy.orm import Session


router = APIRouter(
    tags=["person"]
)
get_db = database.get_db


@router.post("/person", response_model=schema.ShowPerson, status_code=status.HTTP_201_CREATED)
def create_person(request: schema.Person, db: Session = Depends(get_db)):
    new_person = models.Person(name=request.name, email=request.email,
                               phone=request.phone, address=request.address, password=request.password)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person
