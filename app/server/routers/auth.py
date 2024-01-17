from fastapi import APIRouter


router = APIRouter(prefix='/auth')


@router.get(path='/signup/')
async def create_user():
    return "Usuario creado"