from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.database import Base

class Evento(Base):
    __tablename__ = "eventos_processados"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, nullable=False)
    processado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))