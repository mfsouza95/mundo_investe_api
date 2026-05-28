from sqlalchemy.orm import Session
from app.models.cliente import Cliente

def criar_cliente(db: Session, nome: str, email: str, tipo_solicitacao: str, valor_patrimonio: float):
    cliente_objeto = Cliente(nome = nome, email = email, tipo_solicitacao = tipo_solicitacao, valor_patrimonio = valor_patrimonio)
    db.add(cliente_objeto)
    db.commit()
    db.refresh(cliente_objeto)
    return cliente_objeto
            
def buscar_cliente_por_email(db: Session, email: str):
    return db.query(Cliente).filter(Cliente.email == email).first()

def atualizar_cliente(db: Session, cliente:Cliente, status:str, prioridade:str):
    cliente.status = status # type: ignore
    cliente.prioridade = prioridade # type: ignore
    db.commit()
    db.refresh(cliente)
    return cliente