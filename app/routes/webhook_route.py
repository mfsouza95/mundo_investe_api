from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.webhook import WebhookCardUpdated
from app.schemas.cliente import ClienteResponse
from app.services.cliente_service import processar_webhook

router = APIRouter()
@router.post("/webhooks/pipefy/card-updated", response_model=ClienteResponse)
def atualizar_card(dados: WebhookCardUpdated, db: Session = Depends(get_db)):
    update = processar_webhook(db, dados)
    return update