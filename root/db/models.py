from datetime import datetime

from sqlalchemy import Column, String, Boolean, Date, Integer, DateTime, ForeignKey, Float, Text, UniqueConstraint, \
    Table, event
from sqlalchemy.orm import DeclarativeBase, relationship

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    
    tg_id = Column(Integer, primary_key=True)
    username = Column(String(100))
    date_registered = Column(DateTime, default=datetime.now)
