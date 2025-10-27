from flask import request, jsonify
from models.database import db
from models.atividades_model import Atividades
from models.notas_model import Notas
from datetime import datetime


def setup_routes(app):
    
    # CRUD ATIVIDADES

    @app.route('/atividades', methods=['GET'])
    def listar_atividades():
        """
        Lista todas as atividades
        ---
        tags:
          - Atividades
        summary: Lista todas as atividades cadastradas
        responses:
          200:
            description: Lista de atividades
        """

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
        """
        Obtém uma atividade pelo ID
        ---
        tags:
          - Atividades
        summary: Recupera uma atividade específica
        parameters:
          - in: path
            name: id
            schema: { type: integer }
            required: true
            description: ID da atividade
        responses:
          200:
            description: Atividade encontrada
          404:
            description: Atividade não encontrada
        """

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
        """
        Cria uma nova atividade
        -----------------------

        tags:
            - Atividades
        summary: Registra uma nova atividade no sistema
        parameters:
            - in: body
            name: body
            required: true
            schema:
                type: object
                required:
                    - nome_atividade
                    - descricao
                    - peso_porcento
                    - data_entrega
                    - turma_id
                    - professor_id
                properties:
                    nome_atividade:
                        type: string
                        example: "Prova de História"
                    descricao:
                        type: string
                        example: "Avaliação sobre a Revolução Francesa"
                    peso_porcento:
                        type: number
                        example: 25
                    data_entrega:
                        type: string
                        format: date
                        example: "2025-11-05"
                    turma_id:
                        type: integer
                        example: 2
                    professor_id:
                        type: integer
                        example: 5
        responses:
            201:
                description: Atividade criada com sucesso
            400:
                description: Formato de data inválido
        """

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
        """
        Atualiza uma atividade existente
        --------------------------------

        tags:
            - Atividades
        summary: Atualiza os dados de uma atividade cadastrada
        parameters:
            - in: path
            name: id
            required: true
                type: integer
                description: ID da atividade que será atualizada
            example: 1
            - in: body
            name: body
            required: true
                schema:
                type: object
                required:
                    - nome_atividade
                    - descricao
                    - peso_porcento
                    - data_entrega
                    - turma_id
                    - professor_id
                properties:
                    nome_atividade:
                        type: string
                        example: "Prova de Matemática - Revisão"
                    descricao:
                        type: string
                        example: "Revisão de conteúdos para a avaliação final"
                    peso_porcento:
                        type: number
                        example: 30
                    data_entrega:
                        type: string
                        format: date
                        example: "2025-11-20"
                    turma_id:
                        type: integer
                        example: 3
                    professor_id:
                        type: integer
                        example: 1
        responses:
            200:
                description: Atividade atualizada com sucesso
            400:
                description: Formato de data inválido
            404:
                description: Atividade não encontrada
        """


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
        """
        Deleta uma Atividade existente
        ---
        tags:
          - Atividades
        summary: Remove uma Atividade do banco de dados
        parameters:
          - in: path
            name: id
            schema: { type: integer }
            required: true
        responses:
          200:
            description: Atividade deletada com sucesso
          404:
            description: Atividade não encontrada
        """

        atv = Atividades.query.get(id)

        if not atv:
            return jsonify({'erro': 'Nenhuma atividade encontrada!'}), 404
        
        db.session.delete(atv)
        db.session.commit()

        return jsonify({'mensagem': 'Atividade deletada com sucesso!'}), 200
    

    # CRUD NOTAS

    @app.route('/notas', methods=['GET'])
    def get_notas():
        """
        Lista todas as notas
        ---
        tags:
          - Notas
        summary: Lista todas as notas cadastradas
        responses:
          200:
            description: Lista de notas
        404:
            description: Nenhuma nota encontrada.
        """

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
        """
        Obtém uma Nota pelo ID
        ---
        tags:
          - Notas
        summary: Recupera uma Nota específica
        parameters:
          - in: path
            name: id
            schema: { type: integer }
            required: true
            description: ID da Nota
        responses:
          200:
            description: Nota encontrada
          404:
            description: Nota não encontrada
        """

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
        """
        Cria uma nova Nota
        -----------------------

        tags:
            - Notas
        summary: Registra uma nova Nota no sistema
        parameters:
            - in: body
            name: body
            required: true
            schema:
                type: object
                required:
                    - nota
                    - aluno_id
                    - atividade_id
                properties:
                    nota:
                        type: float
                        example: 7.5
                    aluno_id:
                        type: integer
                        example: 2
                    atividade_id:
                        type: integer
                        example: 5
        responses:
            201:
                description: Nota criada com sucesso
        """

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
        """
        Atualiza uma atividade existente
        --------------------------------

        tags:
            - Atividades
        summary: Atualiza os dados de uma atividade cadastrada
        parameters:
            - in: path
            name: id
            required: true
                type: integer
                description: ID da atividade que será atualizada
            example: 1
            - in: body
            name: body
            required: true
                schema:
                type: object
                required:
                    - nota
                    - aluno_id
                    - atividade_id
                properties:
                    nota:
                        type: integer
                        example: 7.5
                    aluno_id:
                        type: integer
                        example: 3
                    atividade_id:
                        type: integer
                        example: 1
        responses:
            200:
                description: Nota atualizada com sucesso
            404:
                description: Nota não encontrada
        """

        nota = Notas.query.get(id)

        if not nota:
            return jsonify({'erro': 'Nota não encontrada!'}), 404
        
        dados = request.get_json()

        nota.nota = float(dados['nota'])
        nota.aluno_id = int(dados['aluno_id'])
        nota.atividade_id = int(dados['atividade_id'])

        db.session.commit()

        return jsonify({'mensagem': 'Nota atualizada com sucesso!'}), 200
    
    @app.route('/notas/<int:id>', methods=['DELETE'])
    def delete_nota(id):
        """
        Deleta uma Nota existente
        ---
        tags:
          - Notas
        summary: Remove uma Nota do banco de dados
        parameters:
          - in: path
            name: id
            schema: { type: integer }
            required: true
        responses:
          200:
            description: Nota deletada com sucesso
          404:
            description: Nota não encontrada
        """

        nota = Notas.query.get(id)

        if not nota:
            return jsonify({'erro': 'Nota não encontrada no sistema!'}), 404
        
        db.session.delete(nota)
        db.session.commit()

        return jsonify({'mensagem': 'Nota deletada com sucesso!'}), 200