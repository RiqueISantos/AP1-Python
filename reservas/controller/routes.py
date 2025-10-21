from flask import request, jsonify
from models.reserva_model import db, Reserva

def setup_routes(app):

    # ------------------ CRUD Reservas ------------------

    @app.route('/reservas', methods=['GET'])
    def list_reservas():
        """
        Lista todas as reservas
        ---
        tags:
          - Reservas
        summary: Lista todas as reservas cadastradas
        responses:
          200:
            description: Lista de reservas
        """
        reservas = Reserva.query.all()
        return jsonify([{
            'id': r.id,
            'num_sala': r.num_sala,
            'lab': r.lab,
            'data': r.data,
            'turma_id': r.turma_id
        } for r in reservas]), 200

    @app.route('/reservas', methods=['POST'])
    def create_reserva():
        """
        Cria uma nova reserva
        ---
        tags:
          - Reservas
        summary: Cria uma reserva com base no payload enviado
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  num_sala: { type: string }
                  lab: { type: boolean }
                  data: { type: string }
                  turma_id: { type: integer }
        responses:
          201:
            description: Reserva criada com sucesso
          400:
            description: Dados inválidos
        """
        data = request.get_json()
        r = Reserva(
            num_sala=data.get('num_sala'),
            lab=data.get('lab', False),
            data=data['data'],
            turma_id=data['turma_id']
        )
        db.session.add(r)
        db.session.commit()
        return jsonify({'message': 'Reserva criada', 'id': r.id}), 201

    @app.route('/reservas/<int:id>', methods=['GET'])
    def get_reserva(id):
        """
        Obtém uma reserva pelo ID
        ---
        tags:
          - Reservas
        summary: Recupera uma reserva específica
        parameters:
          - in: path
            name: id
            schema: { type: integer }
            required: true
            description: ID da reserva
        responses:
          200:
            description: Reserva encontrada
          404:
            description: Reserva não encontrada
        """
        r = Reserva.query.get(id)
        if not r:
            return jsonify({'mensagem': 'Reserva não encontrada'}), 404
        return jsonify({
            'id': r.id,
            'num_sala': r.num_sala,
            'lab': r.lab,
            'data': r.data,
            'turma_id': r.turma_id
        }), 200

    @app.route('/reservas/<int:id>', methods=['PUT'])
    def update_reserva(id):
        """
        Atualiza uma reserva existente
        ---
        tags:
          - Reservas
        summary: Atualiza os dados de uma reserva
        parameters:
          - in: path
            name: id
            schema: { type: integer }
            required: true
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  num_sala: { type: string }
                  lab: { type: boolean }
                  data: { type: string }
                  turma_id: { type: integer }
        responses:
          200:
            description: Reserva atualizada com sucesso
          404:
            description: Reserva não encontrada
        """
        r = Reserva.query.get(id)
        if not r:
            return jsonify({'mensagem': 'Reserva não encontrada'}), 404

        data = request.get_json()
        r.num_sala = data.get('num_sala', r.num_sala)
        r.lab = data.get('lab', r.lab)
        r.data = data.get('data', r.data)
        r.turma_id = data.get('turma_id', r.turma_id)
        db.session.commit()
        return jsonify({'message': 'Reserva atualizada'}), 200

    @app.route('/reservas/<int:id>', methods=['DELETE'])
    def delete_reserva(id):
        """
        Deleta uma reserva existente
        ---
        tags:
          - Reservas
        summary: Remove uma reserva do banco de dados
        parameters:
          - in: path
            name: id
            schema: { type: integer }
            required: true
        responses:
          200:
            description: Reserva deletada com sucesso
          404:
            description: Reserva não encontrada
        """
        r = Reserva.query.get(id)
        if not r:
            return jsonify({'mensagem': 'Reserva não encontrada'}), 404
        db.session.delete(r)
        db.session.commit()
        return jsonify({'message': 'Reserva deletada'}), 200
