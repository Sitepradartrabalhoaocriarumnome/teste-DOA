from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/adicionar", response_model=schemas.Recebedor)
def adicionar_recebedor(recebedor: schemas.RecebedorBase, db: Session = Depends(get_db)):
    return crud.create_recebedor(db=db, recebedor=recebedor)
