from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: Optional[int] = None
    name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    date_of_birth: Optional[date]
    create_date: Optional[datetime] = None
    role: Optional[str] = 'user'
    is_active: Optional[bool] = True
    verified: Optional[bool] = False


class Token(BaseModel):
    access_token: str
    token_type: str
