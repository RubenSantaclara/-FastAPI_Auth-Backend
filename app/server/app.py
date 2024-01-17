from fastapi import FastAPI
from fastapi.responses import RedirectResponse


app = FastAPI()


@app.get('/', tags=['Docs'])
async def main():
    return RedirectResponse('/docs')