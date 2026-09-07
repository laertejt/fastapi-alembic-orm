# FastAPI + Alembic + SQLAlchemy ORM

API de cadastro escolar com PostgreSQL, CRUD de alunos e consultas de endereços, disciplinas e notas. O SQLAlchemy faz o mapeamento das tabelas e o Alembic controla as migrações do banco.

## Tecnologias

- Python 3.13 ou superior
- FastAPI e Uvicorn
- SQLAlchemy 2 e Psycopg 3
- Alembic
- PostgreSQL
- uv para gerenciar ambiente e dependências

## Instalação

Na pasta do projeto, com Python e uv instalados:

```bash
uv sync
```

## Banco de dados

A conexão em `app/database.py` usa estes valores:

| Parâmetro | Valor |
|---|---|
| Host | `127.0.0.1` |
| Porta | `5432` |
| Banco | `ibmec` |
| Usuário | `ibmec` |
| Driver SQLAlchemy | `postgresql+psycopg` |
| Senha | Variável `IBMEC_POSTGRES_PASSWORD` |

Crie ou edite o arquivo `.env` na raiz, usando a senha do usuário do banco:

```dotenv
IBMEC_POSTGRES_PASSWORD=sua_senha_do_postgres
```

O `.env` contém credenciais e deve ficar fora do controle de versão. Atualmente, o `.gitignore` deste projeto ainda não inclui esse arquivo.

O banco deve existir antes da execução das migrações. Para usar o container local configurado no projeto vizinho `ibmec`:

```bash
docker compose -f ../ibmec/compose.yaml --project-directory ../ibmec up -d --wait
```

Use no `.env` desta API a mesma senha configurada no `.env` do projeto `ibmec`. Esse Compose é externo a este repositório; em outra máquina, disponibilize uma instância PostgreSQL com os parâmetros acima ou ajuste `app/database.py`.

## Migrações

Com o PostgreSQL disponível, aplique as migrações existentes:

```bash
uv run alembic upgrade head
```

Para consultar a revisão aplicada e o histórico:

```bash
uv run alembic current
uv run alembic history
```

Após alterar os modelos, gere uma nova migração, revise o arquivo produzido e então aplique:

```bash
uv run alembic revision --autogenerate -m "descreve a alteracao"
uv run alembic upgrade head
```

## Execução

Depois de aplicar as migrações:

```bash
uv run uvicorn app.main:app --reload
```

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- Esquema OpenAPI: <http://127.0.0.1:8000/openapi.json>

## Endpoints

| Método | Rota | Operação |
|---|---|---|
| GET | `/alunos/` | Listar alunos |
| GET | `/alunos/{id}` | Buscar aluno pelo ID |
| POST | `/alunos/` | Criar aluno |
| PUT | `/alunos/{id}` | Atualizar os campos enviados com valor diferente de `null` |
| DELETE | `/alunos/{id}` | Excluir aluno |
| GET | `/enderecos/` | Listar endereços |
| GET | `/disciplinas/` | Listar disciplinas |
| GET | `/notas/` | Listar notas |

Na implementação atual, as rotas de coleção terminam com `/`. Acessá-las sem a barra pode gerar um redirecionamento HTTP 307.

### Exemplo de cadastro

No Swagger UI, abra `POST /alunos/`, clique em **Try it out** e envie:

```json
{
  "matricula": "20260001",
  "nome_aluno": "Maria Silva",
  "email": "maria@example.com",
  "endereco_id": null
}
```

A matrícula deve ser única. Se informado, `endereco_id` precisa apontar para um endereço existente. As rotas de busca, atualização e exclusão retornam 404 quando o aluno não existe. Conflitos de integridade no cadastro retornam 400.

O `PUT` aceita atualização parcial, mas ignora valores `null`; portanto, ele ainda não permite limpar `email` ou `endereco_id` enviando `null`.

## Modelo de dados

- `tb_enderecos`: endereço com CEP único.
- `tb_alunos`: aluno com matrícula única e endereço opcional.
- `tb_disciplinas`: nome, carga e semestre da disciplina.
- `tb_notas`: vínculo entre aluno e disciplina, com nota decimal opcional.

Excluir um endereço mantém os alunos e remove a referência ao endereço. Excluir um aluno ou uma disciplina também exclui suas notas vinculadas.

## Estrutura

```text
app/
  main.py             # Aplicação e registro das rotas
  database.py         # Conexão, fábrica de sessões e base ORM
  models.py           # Modelos SQLAlchemy
  schemas.py          # Validação de entrada dos alunos
  routers/
    alunos.py         # CRUD de alunos
    enderecos.py      # Consulta de endereços
    disciplinas.py    # Consulta de disciplinas
    notas.py          # Consulta de notas
alembic/
  env.py              # Integração das migrações com os modelos
  versions/           # Histórico de migrações
alembic.ini
pyproject.toml
uv.lock
```
# fastapi-alembic-orm
