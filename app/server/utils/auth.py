import os
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, date, timedelta
from jose import JWTError, jwt

from server.db import models, schemas

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITH"))
    return encoded_jwt


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def add_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email, 
        hashed_password=hashed_password, 
        create_date=datetime.now()
    )
    db.add(db_user)
    try:    
        db.commit()
        db.refresh(db_user)
        return {'state': 'created', 'email': user.email}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Unexpected error'
        )

