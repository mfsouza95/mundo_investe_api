from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.cliente import ClienteCreate
from app.schemas.webhook import WebhookCardUpdated
from app.services.pipefy_service import montar_mutation_create_card, montar_mutation_update_card
from app.repositories.cliente_repository import criar_cliente, buscar_cliente_por_email, atualizar_cliente
from app.repositories.evento_repository import buscar_evento_por_event_id, criar_evento

def registrar_cliente( db: Session, dados: ClienteCreate ):
    cliente = criar_cliente(
        db = db,
        nome = dados.cliente_nome,
        email = dados.cliente_email,
        tipo_solicitacao = dados.tipo_solicitacao,
        valor_patrimonio = dados.valor_patrimonio
    )
    mutation = montar_mutation_create_card(
        nome=dados.cliente_nome,
        email=dados.cliente_email,
        patrimonio=dados.valor_patrimonio
    )
    print(mutation)
    return cliente

def processar_webhook( db: Session, dados: WebhookCardUpdated ):
    evento = buscar_evento_por_event_id (db, dados.event_id)
    if evento:
        raise HTTPException(status_code = 409, detail = "Evento já processado!")
    cliente = buscar_cliente_por_email(db, dados.cliente_email)
    if not cliente:
        raise HTTPException(status_code = 404, detail = "Email não encontrado!")
    if cliente.valor_patrimonio >= 200000: # type: ignore
        prioridade = "prioridade_alta"
    else:
        prioridade = "prioridade_normal"
    atualizar_cliente(db, cliente, "Processado", prioridade)
    criar_evento(db, dados.event_id)
    mutation = montar_mutation_update_card(
        card_id=dados.card_id,
        status="Processado",
        prioridade=prioridade
    )
    print(mutation)
    return cliente