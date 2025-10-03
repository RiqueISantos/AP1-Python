# 📚 Escola API

Este projeto é uma API de microsserviços para cadastro e gerenciamento de **alunos**, **turmas** e **professores**. A aplicação foi desenvolvida em Python utilizando Flask, Flask-SQLAlchemy e Flasgger para documentação automática das rotas. O ambiente é facilmente executável via Docker.

## 🚀 Funcionalidades

- Cadastro, listagem, atualização e remoção de **alunos**
- Cadastro, listagem, atualização e remoção de **professores**
- Cadastro, listagem, atualização e remoção de **turmas**
- Relacionamento entre alunos, turmas e professores
- Documentação automática das rotas via Swagger (Flasgger)

## 🛠️ Tecnologias Utilizadas

- Python 3
- Flask
- SQLAlchemy
- Flasgger (Swagger UI)
- Docker

## 📦 Como Executar

### Pré-requisitos

- [Docker](https://www.docker.com/) instalado

### Passos

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/escola-api.git
   
Construa e suba o container:

docker compose up --build

Acesse a API:

A API estará disponível em: http://localhost:5000
A documentação Swagger estará em: http://localhost:5000/apidocs


📑 Exemplos de Rotas

**Professores**
GET /professores — Lista todos os professores
POST /professores — Cria um novo professor
PUT /professores/<id> — Atualiza um professor
DELETE /professores/<id> — Remove um professor

**Turmas**
GET /turmas — Lista todas as turmas
POST /turmas — Cria uma nova turma
PUT /turmas/<id> — Atualiza uma turma
DELETE /turmas/<id> — Remove uma turma

**Alunos**
GET /alunos — Lista todos os alunos
POST /alunos — Cria um novo aluno
PUT /alunos/<id> — Atualiza um aluno
DELETE /alunos/<id> — Remove um aluno


🗂️ Estrutura do Projeto

escola-api/
│
├── app.py
├── controller/
│   └── route.py
├── models/
│   ├── __init__.py
│   ├── aluno_model.py
│   ├── professor_model.py
│   ├── turma_model.py
│   └── database.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md


📝 Observações
O banco de dados utilizado é SQLite e o arquivo database.db é persistido no volume do Docker.
As configurações sensíveis (como SECRET_KEY) são geradas automaticamente, mas podem ser ajustadas conforme necessário.


📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.