from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from server.db import models
from server.db.database import SessionLocal, engine
from server.routers import auth

models.Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()

app.include_router(router=auth.router)


@app.get('/', tags=['Docs'])
async def main():
    return RedirectResponse('/docs')