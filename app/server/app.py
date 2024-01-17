from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from server.routers import auth


app = FastAPI()

app.include_router(router=auth.router)


@app.get('/', tags=['Docs'])
async def main():
    return RedirectResponse('/docs')