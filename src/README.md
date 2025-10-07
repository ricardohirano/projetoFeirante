# 🧠 Estrutura do Diretório `src/` — Backend Vitrine de Feiras

Este diretório contém o **código-fonte principal** do backend da aplicação **Vitrine de Feiras**, estruturado segundo o padrão **MVC (Model–View–Controller)** adaptado para **APIs Flask**.

---

## 🗂️ Estrutura de Pastas
📁 src/  
│ ├── app.py → ponto de entrada da aplicação (App Factory Flask)  
│ ├── controllers/ → controladores (rotas HTTP)  
│ ├── services/ → regras de negócio (CRUD, validações)  
│ ├── models/ → modelos ORM (SQLAlchemy → MySQL)  
│ ├── schemas/ → validação de dados (Pydantic ou Marshmallow)  
│ └── core/ → configurações globais (CORS, logs, etc)

## ⚙️ Arquitetura e Responsabilidades

| Camada | Localização | Função Principal | Exemplo |
|:-------|:-------------|:----------------|:---------|
| **Model** | `models/` | Define entidades, colunas e relacionamentos no banco | Classe `Produto` com SQLAlchemy |
| **Service** | `services/` | Implementa regras de negócio e lógica de manipulação | Funções `criar()`, `atualizar_parcial()` |
| **Controller** | `controllers/` | Recebe requisições HTTP e retorna respostas JSON | Rota `POST /produtos/` |
| **View** | (Integrada ao Flask) | Resposta JSON para o frontend | `return jsonify(produto)` |

> 🧩 *No backend, a “View” é a resposta JSON.  
> A interface visual (HTML/JS) pertence ao módulo **frontend** do projeto.*

---

## 🧭 Convenções de Desenvolvimento

- **Controllers** não contêm lógica de negócio — apenas chamam os *services*.  
- **Services** não conhecem o Flask — apenas manipulam dados e regras.  
- **Models** representam entidades do banco e são gerenciados via **SQLAlchemy**.  
- **Schemas** validam dados de entrada/saída e garantem integridade da API.  
- **Core** centraliza configurações comuns, como logs, CORS, JWT e conexões.


