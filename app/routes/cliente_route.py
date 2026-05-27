from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.services.cliente_service import registrar_cliente

router = APIRouter()

@router.post("/clientes", response_model = ClienteResponse)
def criacao_cliente(dados: ClienteCreate, db: Session = Depends(get_db)):
    cliente = registrar_cliente(db, dados)
    return cliente