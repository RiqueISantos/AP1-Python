from flask import request, jsonify
from models.professor_model import Professor
from models.aluno_model import Aluno
from models.turma_model import Turma
from models.database import db
from datetime import datetime

def setup_routes(app):

    # ----- CRUD Professor -----
    @app.route('/professores', methods=['POST'])
    def create_professor():
        data = request.json
        professor = Professor(**data)
        db.session.add(professor)
        db.session.commit()
        return jsonify({'id': professor.id}), 201

    @app.route('/professores', methods=['GET'])
    def get_professores():
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
        data = request.json
        professor = Professor.query.get_or_404(id)
        for key, value in data.items():
            setattr(professor, key, value)
        db.session.commit()
        return jsonify({'message': 'Professor atualizado'})

    @app.route('/professores/<int:id>', methods=['DELETE'])
    def delete_professor(id):
        professor = Professor.query.get_or_404(id)
        db.session.delete(professor)
        db.session.commit()
        return jsonify({'message': 'Professor deletado'})


    # ----- CRUD Turma -----
    @app.route('/turmas', methods=['POST'])
    def create_turma():
        data = request.json
        turma = Turma(**data)
        db.session.add(turma)
        db.session.commit()
        return jsonify({'id': turma.id}), 201

    @app.route('/turmas', methods=['GET'])
    def get_turmas():
        turmas = Turma.query.all()
        return jsonify([{
            'id': t.id,
            'descricao': t.descricao,
            'professor_id': t.professor_id,
            'ativo': t.ativo
        } for t in turmas])

    @app.route('/turmas/<int:id>', methods=['PUT'])
    def update_turma(id):
        data = request.json
        turma = Turma.query.get_or_404(id)
        for key, value in data.items():
            setattr(turma, key, value)
        db.session.commit()
        return jsonify({'message': 'Turma atualizada'})

    @app.route('/turmas/<int:id>', methods=['DELETE'])
    def delete_turma(id):
        turma = Turma.query.get_or_404(id)
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'message': 'Turma deletada'})


    # ----- CRUD Aluno -----
    @app.route('/alunos', methods=['POST'])
    def create_aluno():
        data = request.json
        if 'data_nascimento' in data:
            data['data_nascimento'] = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        aluno = Aluno(**data)
        db.session.add(aluno)
        db.session.commit()
        return jsonify({'id': aluno.id}), 201

    @app.route('/alunos', methods=['GET'])
    def get_alunos():
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
        aluno = Aluno.query.get_or_404(id)
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({'message': 'Aluno deletado'})
