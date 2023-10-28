import os

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, pool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from root.db import models

load_dotenv(find_dotenv())

engine = create_engine(
        f'{os.getenv("DB_ENGINE")}://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}',
        poolclass=pool.QueuePool, pool_size=10, max_overflow=20, pool_pre_ping=True)

Session = sessionmaker(
    bind=engine,
)

if __name__ == '__main__':
    models.User.__table__.create(bind=engine)
    pass
