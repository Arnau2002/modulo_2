from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base de datos SQLite en memoria o archivo
DATABASE_URL = "sqlite:///./videoclub.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

