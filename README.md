# 🏫 Sistema de Gestão Escolar - Microsserviços

Este projeto consiste em um sistema de gestão escolar baseado em **arquitetura de microsserviços**, desenvolvido em **Python com Flask**.  
O sistema permite o **cadastro e gerenciamento de alunos, turmas, professores, reservas de salas/laboratórios e controle de atividades/notas**.

---

## 📚 Sumário
- [Visão Geral](#visão-geral)
- [Microsserviços](#microsserviços)
- [Arquitetura](#arquitetura)
- [Como Executar](#como-executar)
- [Rotas Principais](#rotas-principais)
- [Exemplo de Uso](#exemplo-de-uso)
- [Documentação Swagger](#documentação-swagger)
- [Dependências](#dependências)
- [Observações](#observações)

---

## 🔎 Visão Geral
O sistema é composto por três microsserviços principais:

1. **Gerenciamento:** Cadastro e consulta de alunos, turmas e professores.  
2. **Atividades-Notas:** Gerenciamento de atividades e notas dos alunos.  
3. **Reservas:** Gerenciamento de reservas de salas e laboratórios para turmas.  

Cada serviço possui sua própria base de dados e expõe **APIs RESTful** para integração.

---

## ⚙️ Microsserviços

### 1. Gerenciamento
Responsável pelo cadastro e consulta de:
- Alunos  
- Turmas  
- Professores  

### 2. Atividades-Notas
Responsável por:
- Cadastro de atividades  
- Lançamento e consulta de notas dos alunos  

### 3. Reservas
Responsável por:
- Cadastro, consulta, atualização e remoção de reservas de salas/laboratórios  
- Integração com o serviço de **Gerenciamento** para validação de turmas

## 🧩 Arquitetura

+-------------------+ +---------------------+ +------------------+
| Gerenciamento |<---->| Atividades-Notas |<---->| Reservas |
+-------------------+ +---------------------+ +------------------+
^ ^ ^
| | |
+------------------------+-----------------------------+
(Comunicação via HTTP/REST)


Cada microsserviço roda em um **container Docker separado**, e a comunicação entre eles é feita via **HTTP**.

---

## 🚀 Como Executar

### 🔧 Pré-requisitos
- Docker  
- Docker Compose  

### 🪜 Passos

1. **Clone este repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd <nome-do-repositorio>

2. **Execute todos os microsserviços com Docker Compose:**
   ```bash
   docker-compose up --build

3. **Acesse os serviços nas seguintes portas:**

   Gerenciamento → http://localhost:5000

   Reservas → http://localhost:5001

   Atividades-Notas → http://localhost:5002

### 🌐 Rotas Principais

🧾 Gerenciamento
Método	     Rota                  Descrição
GET	    /alunos	               Lista alunos
POST	    /alunos	               Cria aluno
GET	    /turmas	               Lista turmas
POST	    /turmas	               Cria turma
GET	    /professores	         Lista professores
POST 	    /professores	         Cria professor

### 🧮 Atividades-Notas
Método	      Rota	               Descrição
GET	    /atividades	         Lista atividades
POST	    /atividades	         Cria atividade
GET	    /notas	               Lista notas
POST	    /notas	               Lança nota

### 🏫 Reservas
Método	      Rotas	               Descrição
GET	    /reservas	            Lista reservas
POST	    /reservas	            Cria reserva (valida turma no Gerenciamento)
GET	    /reservas/<id>	      Consulta reserva por ID
PUT	    /reservas/<id>	      Atualiza reserva
DELETE	 /reservas/<id>	      Remove reserva

### 💻 Exemplo de Uso

Criar uma nova reserva (requisição para o serviço Reservas):

   POST /reservas
   Content-Type: application/json

   {
      "num_sala": 101,
      "lab": true,
      "data": "2025-10-22",
      "turma_id": 1
   }

### 📖 Documentação Swagger

Cada microsserviço expõe sua documentação interativa via Swagger:

Gerenciamento →    http://localhost:5000/apidocs

Atividades-Notas → http://localhost:5001/apidocs

Reservas →         http://localhost:5002/apidocs

### 🧰 Dependências

Principais bibliotecas utilizadas (em cada microsserviço):

Flask
Flask-SQLAlchemy
Flasgger (Swagger UI)
Requests (para comunicação entre serviços)

## Instale as dependências localmente com:

   ```bash
   pip install -r requirements.txt
   ```

## 📝 Observações

Cada microsserviço possui seu próprio banco SQLite.

A comunicação entre os serviços é feita via HTTP interno (ex: o serviço Reservas consulta o Gerenciamento para validar turmas).

Para ambiente produtivo, recomenda-se:

uso de bancos externos (ex: PostgreSQL, MySQL);

configuração de variáveis de ambiente seguras;

uso de Docker networks dedicadas.

O projeto segue uma arquitetura desacoplada, facilitando manutenção e escalabilidade.