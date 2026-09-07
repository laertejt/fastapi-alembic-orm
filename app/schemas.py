from pydantic import BaseModel
from typing import Optional

class AlunoCreate(BaseModel):
    matricula: str
    nome_aluno: str
    email: Optional[str] = None
    endereco_id: Optional[int] = None


class AlunoUpdate(BaseModel):
    matricula: Optional[str] = None
    nome_aluno: Optional[str] = None
    email: Optional[str] = None
    endereco_id: Optional[int] = None