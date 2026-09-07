# uv add psycopg[binary]
# uv run alembic init alembic
# uv run alembic revision --autogenerate -m "cria tabela alunos"
# uv run alembic upgrade head
# uv run alembic history
# uv run alembic current
from typing import Optional
from decimal import Decimal
from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Endereco(Base):
    __tablename__ = "tb_enderecos"
    id: Mapped[int] = mapped_column(primary_key=True)
    cep: Mapped[str] = mapped_column(String(10), unique=True)
    endereco: Mapped[str] = mapped_column(String(255))
    bairro: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    cidade: Mapped[str] = mapped_column(String(100))
    estado: Mapped[str] = mapped_column(String(50))
    regiao: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

class Aluno(Base):
    __tablename__ = "tb_alunos"
    id: Mapped[int] = mapped_column(primary_key=True)
    matricula: Mapped[str] = mapped_column(String(20), unique=True)
    nome_aluno: Mapped[str] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    endereco_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("tb_enderecos.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True
    )

class Disciplina(Base):
    __tablename__ = "tb_disciplinas"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome_disciplina: Mapped[str] = mapped_column(String(255))
    carga: Mapped[int]
    semestre: Mapped[int]

class Nota(Base):
    __tablename__ = "tb_notas"
    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(
        ForeignKey("tb_alunos.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    disciplina_id: Mapped[int] = mapped_column(
        ForeignKey("tb_disciplinas.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    nota: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(5, 2),
        nullable=True
    )