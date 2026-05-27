from pydantic import BaseModel, EmailStr
from datetime import datetime

class WebhookCardUpdated(BaseModel):
    event_id: str
    card_id: str
    cliente_email: EmailStr
    timestamp: datetime