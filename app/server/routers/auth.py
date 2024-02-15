import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime, date, timedelta

from server.db import models, schemas
from server.db.schemas import Token
from server.utils.auth import *
from server.db.database import SessionLocal


router = APIRouter(prefix='/auth')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(path='/signup', status_code=status.HTTP_201_CREATED)
async def create_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=form_data.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail='Email already registered'
        )
    user = schemas.UserCreate(email=form_data.username, password=form_data.password)
    return add_user(db=db, user=user)


@router.post(path='/token', response_model=schemas.Token)
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:    
    db_user = get_user_by_email(db, email=form_data.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    valid_user = verify_password(form_data.password, db_user.hashed_password)
    if not valid_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(
        data = {'sub': db_user.email},
        expires_delta = access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')
    
    
