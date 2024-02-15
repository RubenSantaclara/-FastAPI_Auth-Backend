from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    date_of_birth = Column(Date)
    hashed_password = Column(String)
    create_date = Column(DateTime)
    role = Column(String, default='user')
    is_active = Column(Boolean, default=True)
    verified = Column(Boolean, default=False)

''' 
If need relationships:

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
'''