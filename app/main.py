from fastapi import FastAPI
from app.routers import alunos, enderecos, disciplinas, notas

app = FastAPI()

app.include_router(alunos.router)
app.include_router(enderecos.router)
app.include_router(disciplinas.router)
app.include_router(notas.router)