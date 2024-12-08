from pydantic import BaseModel

class DoadorBase(BaseModel):
    nome: str
    idade: int
    tipo_sanguineo: str
    data_da_ultima_doacao: str

class Doador(DoadorBase):
    id: int

    class Config:
        from_attributes = True

class RecebedorBase(BaseModel):
    nome: str
    idade: int
    tipo_sanguineo: str
    necessidades_de_sangue: str

class Recebedor(RecebedorBase):
    id: int

    class Config:
        from_attributes = True

class DoacaoBase(BaseModel):
    doador_id: int
    recebedor_id: int

class Doacao(DoacaoBase):
    id: int

    class Config:
        from_attributes = True
