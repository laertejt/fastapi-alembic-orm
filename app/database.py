import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
load_dotenv()
senha = os.getenv("IBMEC_POSTGRES_PASSWORD")
DATABASE_URL = f"postgresql+psycopg://ibmec:{senha}@127.0.0.1:5432/ibmec"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    with SessionLocal() as db:
        yield db
