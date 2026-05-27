from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

class ClienteCreate(BaseModel):
    cliente_nome:str
    cliente_email:EmailStr
    tipo_solicitacao:str
    valor_patrimonio:float

    @field_validator('cliente_nome', 'tipo_solicitacao')
    @classmethod
    def handle_empty(cls, v):
        if not v.strip():
            raise ValueError('Campo não pode ser vazio')
        return v

class ClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id: int
    nome: str
    email: str
    tipo_solicitacao: str
    valor_patrimonio: float
    status: str
    prioridade: str | None