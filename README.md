# feira_backend

Backend em **Flask + MySQL** para o sistema **Vitrine de Feiras**.

## 🧩 Stack principal

| Categoria | Tecnologia | Versão | Status |
|------------|-------------|---------|---------|
| Linguagem  | **Python** | 3.14.0 | ✅ configurado |
| Framework  | **Flask** | 3.1.2 | ✅ configurado |
| ORM        | **SQLAlchemy** | 2.x | 🔜 pendente |
| Migrations | **Alembic** | — | 🔜 pendente |
| Banco de Dados | **MySQL 8 (utf8mb4)** | — | 🔜 pendente |
| Autenticação | **JWT + bcrypt** | — | 🔜 pendente |
| Validação | **Pydantic** | — | 🔜 pendente |
| Testes | **Pytest** | — | 🔜 pendente |
| Qualidade de Código | **Ruff + Black + pre-commit** | — | ✅ configurado |
| Documentação | **OpenAPI (flask-apispec)** | — | 🔜 pendente |
| Infraestrutura Dev | **Docker Compose (app, db, adminer, .env)** | — | 🔜 pendente |

---
## 🧩 Estrutura do Código-Fonte (`src/`)

O backend segue o padrão **MVC (Model–View–Controller)** adaptado para APIs Flask.

| Camada | Função | Local |
|--------|---------|--------|
| **Model** | Define entidades e tabelas com SQLAlchemy | `src/models/` |
| **Service** | Implementa regras de negócio | `src/services/` |
| **Controller** | Gera endpoints e responde HTTP (JSON) | `src/controllers/` |
| **View** | No backend, é a resposta JSON para o frontend | — |

📘 [Ver README técnico da pasta `src/`](./src/README.md)

## 🚀 Executar localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install flask ruff black pre-commit
pre-commit install
python -m flask --app src.app run --debug
