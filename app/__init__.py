from fastapi import FastAPI
from .api import api_router
from app.db.base import init_db

app = FastAPI()
app.include_router(api_router)

@app.on_event("startup")
async def on_startup():
    await init_db()