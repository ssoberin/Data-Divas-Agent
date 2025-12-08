from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
import os

# URL подключения (измените credentials если нужно)
DATABASE_URL="postgresql+psycopg2://snow_user:mypassword@localhost:5435/snow_db"

# Создаем engine (синхронный для простоты MVP)
engine = create_engine(DATABASE_URL, echo=True)  # echo=True для логов в dev

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
