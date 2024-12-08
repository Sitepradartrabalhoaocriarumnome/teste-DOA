from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Recebedor])
def listar_recebedores(db: Session = Depends(get_db)):
    return db.query(models.Recebedor).all()

@router.post("/adicionar", response_model=schemas.Recebedor)
def adicionar_recebedor(recebedor: schemas.RecebedorBase, db: Session = Depends(get_db)):
    return crud.create_recebedor(db=db, recebedor=recebedor)

@router.put("/atualizar/{recebedor_id}", response_model=schemas.Recebedor)
def atualizar_recebedor(recebedor_id: int, recebedor: schemas.RecebedorBase, db: Session = Depends(get_db)):
    recebedor_existente = crud.get_recebedor(db, recebedor_id)
    if not recebedor_existente:
        raise HTTPException(status_code=404, detail="Recebedor não encontrado")
    return crud.update_recebedor(db=db, recebedor_id=recebedor_id, recebedor=recebedor)

@router.delete("/excluir/{recebedor_id}")
def deletar_recebedor(recebedor_id: int, db: Session = Depends(get_db)):
    recebedor_existente = crud.get_recebedor(db, recebedor_id)
    if not recebedor_existente:
        raise HTTPException(status_code=404, detail="Recebedor não encontrado")
    crud.delete_recebedor(db=db, recebedor_id=recebedor_id)
    return {"message": f"Recebedor {recebedor_id} deletado com sucesso"}
