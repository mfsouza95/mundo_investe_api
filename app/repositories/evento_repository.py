from sqlalchemy.orm import Session
from app.models.evento import Evento

def buscar_evento_por_event_id(db: Session, event_id: str):
    return db.query(Evento).filter(Evento.event_id == event_id).first()

def criar_evento(db: Session, event_id:str):
    cliente_evento = Evento(event_id = event_id)
    db.add(cliente_evento)
    db.commit()
    db.refresh(cliente_evento)
    return cliente_evento