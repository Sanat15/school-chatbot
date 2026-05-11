from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/school_db")

# Serverless environments (Vercel) cannot hold persistent connection pools.
_is_serverless = bool(os.getenv("VERCEL"))

engine = create_engine(
    DATABASE_URL,
    **({} if _is_serverless else {
        "pool_size": 5,
        "max_overflow": 10,
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }),
    **({"poolclass": NullPool} if _is_serverless else {}),
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()