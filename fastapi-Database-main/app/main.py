from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database
from fastapi.middleware.cors import CORSMiddleware
from .database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8000",
]
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/teste")
def teste_post(data: dict):
    return {"mensagem": "Requisição POST recebida", "dados": data}

@app.post("/doadores/adicionar", response_model=schemas.Doador)
def adicionar_doador(doador: schemas.DoadorBase, db: Session = Depends(get_db)):
    return crud.create_doador(db=db, doador=doador)

@app.post("/recebedores/adicionar", response_model=schemas.Recebedor)
def adicionar_recebedor(recebedor: schemas.RecebedorBase, db: Session = Depends(get_db)):
    return crud.create_recebedor(db=db, recebedor=recebedor)

@app.post("/doacao", response_model=schemas.Doacao)
def realizar_doacao(doacao: schemas.DoacaoBase, db: Session = Depends(get_db)):
    doador = crud.get_doador(db, doacao.doador_id)
    recebedor = crud.get_recebedor(db, doacao.recebedor_id)

    if not doador:
        raise HTTPException(status_code=404, detail="Doador não encontrado")
    if not recebedor:
        raise HTTPException(status_code=404, detail="Recebedor não encontrado")

        tabela_de_compatibilidade_sanguinea = {
        "O-": {"doa_para": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], "recebe_de": ["O-"]},
        "O+": {"doa_para": ["A+", "B+", "AB+", "O+"], "recebe_de": ["O+", "O-"]},
        "A-": {"doa_para": ["A+", "A-", "AB+", "AB-"], "recebe_de": ["A-", "O-"]},
        "A+": {"doa_para": ["A+", "AB+"], "recebe_de": ["A+", "A-", "O+", "O-"]},
        "B-": {"doa_para": ["B+", "B-", "AB+", "AB-"], "recebe_de": ["B-", "O-"]},
        "B+": {"doa_para": ["B+", "AB+"], "recebe_de": ["B+", "B-", "O+", "O-"]},
        "AB-": {"doa_para": ["AB+", "AB-"], "recebe_de": ["A-", "B-", "AB-", "O-"]},
        "AB+": {"doa_para": ["AB+"], "recebe_de": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]},
        "Rh-nulo": {"doa_para": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Rh-nulo"], "recebe_de": ["Rh-nulo"]},
    }

    tipo_doador = doador.tipo_sanguineo
    tipo_recebedor = recebedor.tipo_sanguineo

    if tipo_recebedor not in   tabela_de_compatibilidade_sanguinea[tipo_doador]["doa_para"]:
        raise HTTPException(
            status_code=400,
            detail=f"Incompatibilidade: {tipo_doador} não pode doar para {tipo_recebedor}"
        )

    if tipo_doador not in   tabela_de_compatibilidade_sanguinea[tipo_recebedor]["recebe_de"]:
        raise HTTPException(
            status_code=400,
            detail=f"Incompatibilidade: {tipo_recebedor} não pode receber de {tipo_doador}"
        )

    return {"mensagem": f"Doação compatível de {doador.nome} para {recebedor.nome}"}

    return crud.create_doacao(db=db, doacao=doacao)
