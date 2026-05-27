from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    tipo_solicitacao = Column(String, nullable=False)
    valor_patrimonio = Column(Float, nullable=False)
    status = Column(String, default="Aguardando Análise")
    prioridade = Column(String, nullable=True)
    class Config:
        from_attributes = True