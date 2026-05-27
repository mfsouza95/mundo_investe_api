# Mundo Invest API

API REST desenvolvida em Python com FastAPI para gerenciamento de clientes e integração com o Pipefy via GraphQL.

---

## Tecnologias

- **Python 3.14**
- **FastAPI** — framework web
- **SQLAlchemy** — ORM para banco de dados
- **SQLite** — banco de dados local
- **Pydantic** — validação de payloads
- **pytest** — testes automatizados

---

## Estrutura do Projeto

```
mundo-invest-api/
├── app/
│   ├── models/         # Tabelas do banco de dados
│   ├── schemas/        # Validação de payloads (Pydantic)
│   ├── repositories/   # Queries no banco de dados
│   ├── services/       # Regras de negócio + mutations GraphQL
│   └── routes/         # Endpoints da API
├── tests/
│   └── test_api.py     # Testes automatizados
├── main.py             # Ponto de entrada da aplicação
└── README.md
```

---

## Como executar localmente

### Pré-requisitos

- Python 3.12+
- pip

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/mundo-invest-api.git
cd mundo-invest-api
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`
A documentação interativa estará em `http://127.0.0.1:8000/docs`

---

## Variáveis de Ambiente

| Variável | Descrição | Padrão |
|---|---|---|
| `PIPEFY_PIPE_ID` | ID do pipe no Pipefy | `"SEU_PIPE_ID"` |

---

## Como executar os testes

```bash
pytest tests/test_api.py -v
```

Resultado esperado:
```
tests/test_api.py::test_criar_cliente PASSED
tests/test_api.py::test_prioridade_webhook PASSED
tests/test_api.py::test_duplicidade PASSED
3 passed in 0.73s
```

---

## Endpoints

### POST /clientes

Cria um novo cliente e mapeia um card no Pipefy.

**Payload:**
```json
{
    "cliente_nome": "João Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": 250000
}
```

**Exemplo com curl:**
```bash
curl -X POST http://127.0.0.1:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_nome": "João Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": 250000
  }'
```

**Resposta:**
```json
{
    "id": 1,
    "nome": "João Silva",
    "email": "joao.silva@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": 250000.0,
    "status": "Aguardando Análise",
    "prioridade": null
}
```

---

### POST /webhooks/pipefy/card-updated

Simula o recebimento de um webhook do Pipefy quando um card é atualizado.

**Regras de negócio:**
- `valor_patrimonio >= 200.000` → `prioridade_alta`
- `valor_patrimonio < 200.000` → `prioridade_normal`
- Eventos duplicados são bloqueados via idempotência pelo `event_id`

**Payload:**
```json
{
    "event_id": "evt_123",
    "card_id": "card_456",
    "cliente_email": "joao.silva@example.com",
    "timestamp": "2026-05-18T12:00:00Z"
}
```

**Exemplo com curl:**
```bash
curl -X POST http://127.0.0.1:8000/webhooks/pipefy/card-updated \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_123",
    "card_id": "card_456",
    "cliente_email": "joao.silva@example.com",
    "timestamp": "2026-05-18T12:00:00Z"
  }'
```

**Resposta:**
```json
{
    "id": 1,
    "nome": "João Silva",
    "email": "joao.silva@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": 250000.0,
    "status": "Processado",
    "prioridade": "prioridade_alta"
}
```

---

## Visão de Produção (AWS)

Em produção, essa estrutura escalaria da seguinte forma:

### Banco de Dados
O SQLite seria substituído por **Amazon RDS (PostgreSQL)** — gerenciado, com backups automáticos, alta disponibilidade e suporte a múltiplas conexões simultâneas. Para o processamento de webhooks em alta escala, o **DynamoDB** seria uma alternativa para a tabela de eventos processados, dado seu modelo chave-valor e performance em escritas de alta frequência.

### API
A aplicação FastAPI seria containerizada com **Docker** e hospedada no **AWS ECS (Elastic Container Service)** ou convertida para **AWS Lambda** com o adaptador **Mangum** — permitindo execução serverless sem gerenciamento de servidores, com escalonamento automático e cobrança por execução.

### Webhook
O endpoint de webhook seria exposto via **AWS API Gateway**, que gerencia autenticação, rate limiting e throttling. Para processar os eventos de forma assíncrona e resiliente, o API Gateway poderia publicar os eventos em uma fila **AWS SQS**, e uma Lambda consumiria a fila — garantindo que nenhum evento seja perdido mesmo em picos de tráfego.

### Arquitetura final

```
Pipefy
  ↓
API Gateway → SQS → Lambda (processar_webhook)
                        ↓
                    RDS PostgreSQL
```

Essa arquitetura garante:
- **Escalabilidade** — Lambda escala automaticamente
- **Resiliência** — SQS garante que nenhum evento se perde
- **Idempotência** — mantida via DynamoDB ou RDS
- **Custo** — serverless cobra só pelo uso real
