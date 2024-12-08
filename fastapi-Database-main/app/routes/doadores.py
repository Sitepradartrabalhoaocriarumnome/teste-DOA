from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/adicionar", response_model=schemas.Doador)
def adicionar_doador(doador: schemas.DoadorBase, db: Session = Depends(get_db)):
    return crud.create_doador(db=db, doador=doador)
