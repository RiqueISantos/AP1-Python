from flask import request, jsonify
from models.database import db
from models.atividades_model import Atividades
from models.notas_model import Notas


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

        data = request.get_json()

        atv = Atividades(
            nome_atividade=data['nome_atividade'],
            descricao=data['descricao'],
            peso_porcento=float(data['peso_porcento']),
            data_entrega= '',
            turma_id=int(data['turma_id']),
            professor_id=int(data['professor_id'])
        )

        db.session.add(atv)
        db.session.commit()

        return jsonify({'mensagem': 'Atividade criada!', 'id': atv.id}), 201