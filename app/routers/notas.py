from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Nota

router = APIRouter(prefix="/notas", tags=["Notas"])

def get_db():
    with SessionLocal() as db:
        yield db

@router.get("/")
def listar_notas(db: Session = Depends(get_db)):
    return db.scalars(select(Nota)).all()