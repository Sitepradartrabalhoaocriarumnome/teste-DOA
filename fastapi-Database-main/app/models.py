from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Doador(Base):
    __tablename__ = "doadores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer)
    tipo_sanguineo = Column(String)
    data_da_ultima_doacao = Column(String)

class Recebedor(Base):
    __tablename__ = "recebedores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer)
    tipo_sanguineo = Column(String)
    necessidades_de_sangue = Column(String)

class Doacao(Base):
    __tablename__ = "doacoes"
    id = Column(Integer, primary_key=True, index=True)
    doador_id = Column(Integer, ForeignKey("doadores.id"))
    recebedor_id = Column(Integer, ForeignKey("recebedores.id"))

    doador = relationship("Doador", back_populates="doacoes")
    recebedor = relationship("Recebedor", back_populates="doacoes")

Doador.doacoes = relationship("Doacao", back_populates="doador")
Recebedor.doacoes = relationship("Doacao", back_populates="recebedor")
