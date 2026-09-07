from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Aluno
from app.schemas import AlunoCreate, AlunoUpdate

router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.get("/")
def listar_alunos(db: Session = Depends(get_db)):
    return db.scalars(select(Aluno)).all()

@router.get("/{id}")
def buscar_aluno(id: int, db: Session = Depends(get_db)):
    aluno = db.get(Aluno, id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.post("/")
def criar_aluno(dados: AlunoCreate, db: Session = Depends(get_db)):
    aluno = Aluno(
        matricula=dados.matricula,
        nome_aluno=dados.nome_aluno,
        email=dados.email,
        endereco_id=dados.endereco_id
    )
    try:
        db.add(aluno)
        db.commit()
        db.refresh(aluno)
        return {"message": "Aluno criado com sucesso", "aluno": aluno}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não foi possível criar o aluno")

@router.delete("/{id}")
def deletar_aluno(id: int, db: Session = Depends(get_db)):
    aluno = db.get(Aluno, id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(aluno)
    db.commit()
    return {"message": "Aluno deletado com sucesso"}

@router.put("/{id}")
def atualizar_aluno(id: int, dados: AlunoUpdate, db: Session = Depends(get_db)):
    aluno = db.get(Aluno, id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    if dados.matricula is not None:
        aluno.matricula = dados.matricula
    if dados.nome_aluno is not None:
        aluno.nome_aluno = dados.nome_aluno
    if dados.email is not None:
        aluno.email = dados.email
    if dados.endereco_id is not None:
        aluno.endereco_id = dados.endereco_id
    db.commit()
    db.refresh(aluno)
    return {"message": "Aluno atualizado com sucesso", "aluno": aluno}