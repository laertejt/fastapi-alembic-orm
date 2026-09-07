from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Endereco

router = APIRouter(prefix="/enderecos", tags=["Endereços"])

def get_db():
    with SessionLocal() as db:
        yield db

@router.get("/")
def listar_enderecos(db: Session = Depends(get_db)):
    return db.scalars(select(Endereco)).all()