from sqlalchemy.orm import Session
import models, schemas

def get_doador(db: Session, doador_id: int):
    return db.query(models.Doador).filter(models.Doador.id == doador_id).first()

def get_recebedor(db: Session, recebedor_id: int):
    return db.query(models.Recebedor).filter(models.Recebedor.id == recebedor_id).first()

def create_doador(db: Session, doador: schemas.DoadorBase):
    db_doador = models.Doador(**doador.dict())
    db.add(db_doador)
    db.commit()
    db.refresh(db_doador)
    return db_doador

def create_recebedor(db: Session, recebedor: schemas.RecebedorBase):
    db_recebedor = models.Recebedor(**recebedor.dict())
    db.add(db_recebedor)
    db.commit()
    db.refresh(db_recebedor)
    return db_recebedor

def create_doacao(db: Session, doacao: schemas.DoacaoBase):
    db_doacao = models.Doacao(**doacao.dict())
    db.add(db_doacao)
    db.commit()
    db.refresh(db_doacao)
    return db_doacao