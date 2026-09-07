from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Disciplina

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"])

def get_db():
    with SessionLocal() as db:
        yield db

@router.get("/")
def listar_disciplinas(db: Session = Depends(get_db)):
    return db.scalars(select(Disciplina)).all()