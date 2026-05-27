from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.database import engine, Base
from app.routes.cliente_route import router as cliente_router
from app.routes.webhook_route import router as webhook_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(cliente_router)
app.include_router(webhook_router)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url = "/docs")