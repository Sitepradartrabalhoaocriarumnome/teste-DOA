from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import Base
from .routes import doadores, recebedores, doacoes

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo as rotas
app.include_router(doadores.router, tags=["Doadores"], prefix="/app/doadores")
app.include_router(recebedores.router, tags=["Recebedores"], prefix="/app/recebedores")
app.include_router(doacoes.router, tags=["Doações"], prefix="/app/doacoes")

@app.get("/app/healthchecker")
def root():
    return {"message": "API funcionando com sucesso!"}
