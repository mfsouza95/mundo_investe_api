from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.database import Base, get_db
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(autouse=True)
def limpar_banco():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def test_criar_cliente():
    response = client.post("/clientes", json={
        "cliente_nome": "João Silva",
        "cliente_email": "joao.silva@example.com",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 250000
    })
    assert response.status_code == 200
    assert response.json()["email"] == "joao.silva@example.com"

def test_prioridade_webhook():
    client.post("/clientes", json={ 
        "cliente_nome": "João Silva",
        "cliente_email": "joao.silva@example.com",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 250000
     })
    response = client.post("/webhooks/pipefy/card-updated", json={         
        "event_id": "evt_123",
        "card_id": "card_456",
        "cliente_email": "joao.silva@example.com",
        "timestamp": "2026-05-18T12:00:00Z"
     })
    
    assert response.status_code == 200
    assert response.json()["prioridade"] == "prioridade_alta"

def test_duplicidade():
    client.post("/clientes", json={ 
        "cliente_nome": "João Silva",
        "cliente_email": "joao.silva@example.com",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 250000
     })
    client.post("/webhooks/pipefy/card-updated", json={         
        "event_id": "evt_123",
        "card_id": "card_456",
        "cliente_email": "joao.silva@example.com",
        "timestamp": "2026-05-18T12:00:00Z"
     })
    retry = client.post("/webhooks/pipefy/card-updated", json={         
    "event_id": "evt_123",
    "card_id": "card_456",
    "cliente_email": "joao.silva@example.com",
    "timestamp": "2026-05-18T12:00:00Z"
    })

    assert retry.status_code == 409
    assert retry.json()["detail"] == "Evento já processado!"