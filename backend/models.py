# models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)          # max 100 chars
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255), nullable=False)     # store hashed pwd
    role = Column(String(50), default="buyer")

    favourites = relationship("Favourite", back_populates="user")

class Favourite(Base):
    __tablename__ = "favourites"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    property_name = Column(String(255), nullable=False)  # <--- specify length

    user = relationship("User", back_populates="favourites")