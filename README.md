# feira_backend

Backend em **Flask + MySQL** para o sistema **Vitrine de Feiras**.

## 🧩 Stack principal
- Python 3.12 +
- Flask 3.x
- SQLAlchemy 2.x
- Alembic (migrations)
- MySQL 8 (utf8mb4)
- Auth via JWT + bcrypt
- Validação Pydantic
- Testes Pytest
- Qualidade: Ruff + Black + pre-commit
- Docs: OpenAPI (flask-apispec)
- Infra Dev: Docker Compose (app, db, adminer, .env)

## 🚀 Executar localmente
```bash
python -m venv .venv
.venv\Scripts\activate
pip install flask ruff black pre-commit
pre-commit install
python -m flask --app src.app run --debug
