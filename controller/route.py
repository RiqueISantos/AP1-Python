from flask import request, jsonify, render_template, redirect, url_for, flash
from models.professor_model import Professor
from models.aluno_model import Aluno
from models.turma_model import Turma
from models.database import db
from datetime import datetime

def setup_routes(app):

    # ----- CRUD Professor -----
    @app.route('/professores', methods=['POST'])
    def create_professor():
        """
        Cria um novo professor.
        ---
        tags:
          - Professores
        consumes:
          - application/json
        produces:
          - application/json
        parameters:
          - in: body
            name: professor
            description: Objeto JSON com dados do professor.
            required: true
            schema:
              type: object
              required:
                - nome
                - idade
                - materia
              properties:
                nome:
                  type: string
                  example: "João Silva"
                idade:
                  type: integer
                  example: 45
                materia:
                  type: string
                  example: "Matemática"
                observacoes:
                  type: string
                  example: "Professor titular"
        responses:
          201:
            description: Professor criado com sucesso.
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
        """
        data = request.json
        professor = Professor(**data)
        db.session.add(professor)
        db.session.commit()
        return jsonify({'id': professor.id}), 201

    @app.route('/professores', methods=['GET'])
    def get_professores():
        """
        Lista todos os professores.
        ---
        tags:
          - Professores
        produces:
          - application/json
        responses:
          200:
            description: Lista de professores.
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  nome:
                    type: string
                    example: "João Silva"
                  idade:
                    type: integer
                    example: 45
                  materia:
                    type: string
                    example: "Matemática"
                  observacoes:
                    type: string
                    example: "Professor titular"
        """
        professores = Professor.query.all()
        return jsonify([{
            'id': p.id,
            'nome': p.nome,
            'idade': p.idade,
            'materia': p.materia,
            'observacoes': p.observacoes
        } for p in professores])

    @app.route('/professores/<int:id>', methods=['PUT'])
    def update_professor(id):
        """
        Atualiza dados de um professor pelo ID.
        ---
        tags:
          - Professores
        consumes:
          - application/json
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID do professor a ser atualizado.
          - in: body
            name: professor
            description: Dados para atualizar o professor.
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                  example: "João Silva"
                idade:
                  type: integer
                  example: 46
                materia:
                  type: string
                  example: "Física"
                observacoes:
                  type: string
                  example: "Atualizado para física"
        responses:
          200:
            description: Professor atualizado com sucesso.
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Professor atualizado"
          404:
            description: Professor não encontrado.
        """
        data = request.json
        professor = Professor.query.get_or_404(id)
        for key, value in data.items():
            setattr(professor, key, value)
        db.session.commit()
        return jsonify({'message': 'Professor atualizado'})

    @app.route('/professores/<int:id>', methods=['DELETE'])
    def delete_professor(id):
        """
        Deleta um professor pelo ID.
        ---
        tags:
          - Professores
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID do professor a ser deletado.
        responses:
          200:
            description: Professor deletado com sucesso.
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Professor deletado"
          404:
            description: Professor não encontrado.
        """
        professor = Professor.query.get_or_404(id)
        db.session.delete(professor)
        db.session.commit()
        return jsonify({'message': 'Professor deletado'})


    # ----- CRUD Turma -----
    @app.route('/turmas', methods=['POST'])
    def create_turma():
        """
        Cria uma nova turma.
        ---
        tags:
          - Turmas
        consumes:
          - application/json
        parameters:
          - in: body
            name: turma
            description: Dados da turma.
            required: true
            schema:
              type: object
              required:
                - descricao
                - professor_id
                - ativo
              properties:
                descricao:
                  type: string
                  example: "Turma A"
                professor_id:
                  type: integer
                  example: 1
                ativo:
                  type: boolean
                  example: true
        responses:
          201:
            description: Turma criada com sucesso.
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
        """
        data = request.json
        turma = Turma(**data)
        db.session.add(turma)
        db.session.commit()
        return jsonify({'id': turma.id}), 201

    @app.route('/turmas', methods=['GET'])
    def get_turmas():
        """
        Lista todas as turmas.
        ---
        tags:
          - Turmas
        produces:
          - application/json
        responses:
          200:
            description: Lista de turmas.
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  descricao:
                    type: string
                    example: "Turma A"
                  professor_id:
                    type: integer
                    example: 1
                  ativo:
                    type: boolean
                    example: true
        """
        turmas = Turma.query.all()
        return jsonify([{
            'id': t.id,
            'descricao': t.descricao,
            'professor_id': t.professor_id,
            'ativo': t.ativo
        } for t in turmas])

    @app.route('/turmas/<int:id>', methods=['PUT'])
    def update_turma(id):
        """
        Atualiza dados de uma turma pelo ID.
        ---
        tags:
          - Turmas
        consumes:
          - application/json
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID da turma a ser atualizada.
          - in: body
            name: turma
            description: Dados para atualização da turma.
            required: true
            schema:
              type: object
              properties:
                descricao:
                  type: string
                  example: "Turma B"
                professor_id:
                  type: integer
                  example: 2
                ativo:
                  type: boolean
                  example: false
        responses:
          200:
            description: Turma atualizada com sucesso.
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Turma atualizada"
          404:
            description: Turma não encontrada.
        """
        data = request.json
        turma = Turma.query.get_or_404(id)
        for key, value in data.items():
            setattr(turma, key, value)
        db.session.commit()
        return jsonify({'message': 'Turma atualizada'})

    @app.route('/turmas/<int:id>', methods=['DELETE'])
    def delete_turma(id):
        """
        Deleta uma turma pelo ID.
        ---
        tags:
          - Turmas
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID da turma a ser deletada.
        responses:
          200:
            description: Turma deletada com sucesso.
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Turma deletada"
          404:
            description: Turma não encontrada.
        """
        turma = Turma.query.get_or_404(id)
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'message': 'Turma deletada'})


    # ----- CRUD Aluno -----
    @app.route('/alunos', methods=['POST'])
    def create_aluno():
        """
        Cria um novo aluno.
        ---
        tags:
          - Alunos
        consumes:
          - application/json
        parameters:
          - in: body
            name: aluno
            description: Dados do aluno.
            required: true
            schema:
              type: object
              required:
                - nome
                - idade
                - turma_id
                - data_nascimento
              properties:
                nome:
                  type: string
                  example: "Maria Souza"
                idade:
                  type: integer
                  example: 18
                turma_id:
                  type: integer
                  example: 1
                data_nascimento:
                  type: string
                  format: date
                  example: "2005-05-20"
                nota_primeiro_semestre:
                  type: number
                  format: float
                  example: 8.5
                nota_segundo_semestre:
                  type: number
                  format: float
                  example: 9.0
                media_final:
                  type: number
                  format: float
                  example: 8.75
        responses:
          201:
            description: Aluno criado com sucesso.
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
        """
        data = request.json
        if 'data_nascimento' in data:
            data['data_nascimento'] = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        aluno = Aluno(**data)
        db.session.add(aluno)
        db.session.commit()
        return jsonify({'id': aluno.id}), 201

    @app.route('/alunos', methods=['GET'])
    def get_alunos():
        """
        Lista todos os alunos.
        ---
        tags:
          - Alunos
        produces:
          - application/json
        responses:
          200:
            description: Lista de alunos.
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  nome:
                    type: string
                    example: "Maria Souza"
                  idade:
                    type: integer
                    example: 18
                  turma_id:
                    type: integer
                    example: 1
                  data_nascimento:
                    type: string
                    format: date
                    example: "2005-05-20"
                  nota_primeiro_semestre:
                    type: number
                    format: float
                    example: 8.5
                  nota_segundo_semestre:
                    type: number
                    format: float
                    example: 9.0
                  media_final:
                    type: number
                    format: float
                    example: 8.75
        """
        alunos = Aluno.query.all()
        return jsonify([{
            'id': a.id,
            'nome': a.nome,
            'idade': a.idade,
            'turma_id': a.turma_id,
            'data_nascimento': a.data_nascimento.strftime('%Y-%m-%d'),
            'nota_primeiro_semestre': a.nota_primeiro_semestre,
            'nota_segundo_semestre': a.nota_segundo_semestre,
            'media_final': a.media_final
        } for a in alunos])

    @app.route('/alunos/<int:id>', methods=['PUT'])
    def update_aluno(id):
        """
        Atualiza dados de um aluno pelo ID.
        ---
        tags:
          - Alunos
        consumes:
          - application/json
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID do aluno a ser atualizado.
          - in: body
            name: aluno
            description: Dados para atualização do aluno.
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                  example: "Maria Souza"
                idade:
                  type: integer
                  example: 19
                turma_id:
                  type: integer
                  example: 2
                data_nascimento:
                  type: string
                  format: date
                  example: "2005-05-21"
                nota_primeiro_semestre:
                  type: number
                  format: float
                  example: 9.0
                nota_segundo_semestre:
                  type: number
                  format: float
                  example: 9.5
                media_final:
                  type: number
                  format: float
                  example: 9.25
        responses:
          200:
            description: Aluno atualizado com sucesso.
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Aluno atualizado"
          404:
            description: Aluno não encontrado.
        """
        data = request.json
        aluno = Aluno.query.get_or_404(id)
        if 'data_nascimento' in data:
            data['data_nascimento'] = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        for key, value in data.items():
            setattr(aluno, key, value)
        db.session.commit()
        return jsonify({'message': 'Aluno atualizado'})

    @app.route('/alunos/<int:id>', methods=['DELETE'])
    def delete_aluno(id):
        """
        Deleta um aluno pelo ID.
        ---
        tags:
          - Alunos
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID do aluno a ser deletado.
        responses:
          200:
            description: Aluno deletado com sucesso.
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Aluno deletado"
          404:
            description: Aluno não encontrado.
        """
        aluno = Aluno.query.get_or_404(id)
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({'message': 'Aluno deletado'})
