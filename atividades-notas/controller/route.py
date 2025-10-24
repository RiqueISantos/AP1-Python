from flask import request, jsonify
from models.database import db
from models.atividades_model import Atividades
from models.notas_model import Notas
from datetime import datetime


def setup_routes(app):
    
    # CRUD ATIVIDADES

    @app.route('/atividades', methods=['GET'])
    def listar_atividades():
        """"""

        atividades = Atividades.query.all()

        if not atividades:
            return jsonify({'mensagem': 'Nenhuma atividade cadastrada!'}), 400
        
        return jsonify([{
            'id': atv.id,
            'nome_atividade': atv.nome_atividade,
            'descricao': atv.descricao,
            'peso_porcento': atv.peso_porcento,
            'data_entrega': atv.data_entrega,
            'turma_id': atv.turma_id,
            'professor_id': atv.professor_id
        } for atv in atividades]), 200
    
    @app.route('/atividades/<int:id>', methods=['GET'])
    def get_atividade(id):
        """"""

        atv = Atividades.query.get(id)

        if not atv:
            return jsonify({'mensagem': 'Atividade não encontrada!'}) , 400
        
        return jsonify({
            'id': atv.id,
            'nome_atividade': atv.nome_atividade,
            'descricao': atv.descricao,
            'peso_porcento': atv.peso_porcento,
            'data_entrega': atv.data_entrega,
            'turma_id': atv.turma_id,
            'professor_id': atv.professor_id
        }), 200
    
    @app.route('/atividades', methods=['POST'])
    def create_atividade():
        """"""

        dados = request.get_json()

        try:
            data_entrega = datetime.strptime(dados['data_entrega'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido! Digite no seguinte formato: AAAA-MM-DD. Exemplo: 2025-10-25'}), 400

        atv = Atividades(
            nome_atividade=dados['nome_atividade'],
            descricao=dados['descricao'],
            peso_porcento=float(dados['peso_porcento']),
            data_entrega=data_entrega,
            turma_id=int(dados['turma_id']),
            professor_id=int(dados['professor_id'])
        )

        db.session.add(atv)
        db.session.commit()

        return jsonify({'mensagem': 'Atividade criada!', 'id': atv.id}), 201
    
    @app.route('/atividades/<int:id>', methods=['PUT'])
    def update_atividade(id):
        """"""

        atv = Atividades.query.get(id)

        if not atv:
            return jsonify({'erro': 'Atividade não encontrada!'}), 404
        
        dados = request.get_json()

        try:
            data_entrega = datetime.strptime(dados['data_entrega'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido! Digite no seguinte formato: AAAA-MM-DD. Exemplo: 2025-10-25'}), 400

        atv.nome_atividade = dados['nome_atividade']
        atv.descricao = dados['descricao']
        atv.peso_porcento = float(dados['peso_porcento'])
        atv.data_entrega = data_entrega
        atv.turma_id = dados['turma_id']
        atv.professor_id = dados['professor_id']

        db.session.commit()

        return jsonify({'mensagem': 'Atividade atualizada com sucesso!'}), 200
    
    @app.route('/atividades/<int:id>', methods=['DELETE'])
    def delete_atividade(id):

        atv = Atividades.query.get(id)

        if not atv:
            return jsonify({'erro': 'Nenhuma atividade encontrada!'}), 400
        
        db.session.delete(atv)
        db.session.commit()

        return jsonify({'mensagem': 'Atividade deletada com sucesso!'}), 200
    

    # CRUD NOTAS

    @app.route('/notas', methods=['GET'])
    def get_notas():

        notas = Notas.query.all()
        if not notas:
            return jsonify({'erro': 'Nenhuma nota encontrada no sistema.'}), 404
        
        return jsonify([{
            'id': nota.id,
            'nota': nota.nota,
            'aluno_id': nota.aluno_id,
            'atividade_id': nota.atividade_id
        } for nota in notas]), 200
    
    @app.route('/notas/<int:id>', methods=['GET'])
    def get_nota(id):

        nota = Notas.query.get(id)
        if not nota:
            return jsonify({'erro': 'Nenhuma nota encontrada.'}), 404
        
        return jsonify({
            'id': nota.id,
            'nota': nota.nota,
            'aluno_id': nota.aluno_id,
            'atividade_id': nota.atividade_id
        }), 200
    
    @app.route('/notas', methods=['POST'])
    def create_nota():

        dados = request.get_json()

        nota = Notas(
            nota=float(dados['nota']),
            aluno_id=int(dados['aluno_id']),
            atividade_id=int(dados['atividade_id'])
        )

        db.session.add(nota)
        db.session.commit()

        return jsonify({'mensagem': 'Nota cadastrada com sucesso!'}), 201
    
    @app.route('/notas/<int:id>', methods=['PUT'])
    def update_nota(id):

        nota = Notas.query.get(id)

        if not nota:
            return jsonify({'erro': 'Nota não encontrada!'}), 404
        
        dados = request.get_json()

        nota.nota = float(dados['nota'])
        nota.aluno_id = int(dados['aluno_id'])
        nota.professor_id = int(dados['professor_id'])

        db.session.commit()

        return jsonify({'mensagem': 'Nota atualizada com sucesso!'}), 200
    
    @app.route('/notas/<int:id>', methods=['DELETE'])
    def delete_nota(id):

        nota = Notas.query.get(id)

        if not nota:
            return jsonify({'erro': 'Nota não encontrada no sistema!'}), 404
        
        db.session.delete(nota)
        db.session.commit()

        return jsonify({'mensagem': 'Nota deletada com sucesso!'}), 200