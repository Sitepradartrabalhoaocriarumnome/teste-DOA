from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, models
from database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Doador])
def listar_doadores(db: Session = Depends(get_db)):
    return db.query(models.Doador).all()

@router.post("/adicionar", response_model=schemas.Doador)
def adicionar_doador(doador: schemas.DoadorBase, db: Session = Depends(get_db)):
    return crud.create_doador(db=db, doador=doador)

@router.put("/atualizar/{doador_id}", response_model=schemas.Doador)
def atualizar_doador(doador_id: int, doador: schemas.DoadorBase, db: Session = Depends(get_db)):
    doador_existente = crud.get_doador(db, doador_id)
    if not doador_existente:
        raise HTTPException(status_code=404, detail="Doador não encontrado")
    return crud.update_doador(db=db, doador_id=doador_id, doador=doador)

@router.delete("/excluir/{doador_id}")
def deletar_doador(doador_id: int, db: Session = Depends(get_db)):
    doador_existente = crud.get_doador(db, doador_id)
    if not doador_existente:
        raise HTTPException(status_code=404, detail="Doador não encontrado")
    crud.delete_doador(db=db, doador_id=doador_id)
    return {"message": f"Doador {doador_id} deletado com sucesso"}
