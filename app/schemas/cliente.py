from pydantic import BaseModel, EmailStr, ConfigDict

class ClienteCreate(BaseModel):
    cliente_nome:str
    cliente_email:EmailStr
    tipo_solicitacao:str
    valor_patrimonio:float

class ClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id: int
    nome: str
    email: str
    tipo_solicitacao: str
    valor_patrimonio: float
    status: str
    prioridade: str | None