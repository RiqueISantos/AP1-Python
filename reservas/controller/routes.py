from flask import request
from flask_restx import Namespace, Resource
from models.reserva_model import db, Reserva
from models.schemas import reserva_model

ns = Namespace("reservas", description="Operações de reservas")

@ns.route("")
class ReservaList(Resource):
    @ns.doc("listar_reservas")
    @ns.response(200, "Lista de reservas retornada com sucesso")
    def get(self):
        """
        Lista todas as reservas
        ---
        tags:
          - Reservas
        summary: Recupera todas as reservas cadastradas
        responses:
          200:
            description: Lista de reservas
        """
        reservas = Reserva.query.all()
        return [r.to_dict() for r in reservas], 200

    @ns.expect(reserva_model(ns), validate=True)
    @ns.doc("criar_reserva")
    @ns.response(201, "Reserva criada com sucesso")
    @ns.response(400, "Falha na validação do payload")
    def post(self):
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
              schema: Reserva
        responses:
          201:
            description: Reserva criada com sucesso
          400:
            description: Falha na validação do payload
        """
        payload = request.json
        r = Reserva(
            num_sala=payload.get("num_sala"),
            lab=payload.get("lab", False),
            data=payload["data"],
            turma_id=payload["turma_id"]
        )
        db.session.add(r)
        db.session.commit()
        return r.to_dict(), 201


@ns.route("/<int:id>")
class ReservaResource(Resource):
    @ns.doc("obter_reserva")
    @ns.response(200, "Reserva encontrada")
    @ns.response(404, "Reserva não encontrada")
    def get(self, id):
        """
        Obtém uma reserva pelo ID
        ---
        tags:
          - Reservas
        summary: Recupera uma reserva pelo seu ID
        parameters:
          - in: path
            name: id
            required: true
            schema:
              type: integer
        responses:
          200:
            description: Reserva encontrada
          404:
            description: Reserva não encontrada
        """
        r = Reserva.query.get(id)
        if not r:
            return {"mensagem": "Reserva não encontrada"}, 404
        return r.to_dict(), 200

    @ns.expect(reserva_model(ns), validate=True)
    @ns.doc("atualizar_reserva")
    @ns.response(200, "Reserva atualizada com sucesso")
    @ns.response(404, "Reserva não encontrada")
    def put(self, id):
        """
        Atualiza uma reserva pelo ID
        ---
        tags:
          - Reservas
        summary: Atualiza os dados de uma reserva existente
        parameters:
          - in: path
            name: id
            required: true
            schema:
              type: integer
        requestBody:
          required: true
          content:
            application/json:
              schema: Reserva
        responses:
          200:
            description: Reserva atualizada com sucesso
          404:
            description: Reserva não encontrada
        """
        r = Reserva.query.get(id)
        if not r:
            return {"mensagem": "Reserva não encontrada"}, 404

        payload = request.json
        r.num_sala = payload.get("num_sala", r.num_sala)
        r.lab = payload.get("lab", r.lab)
        r.data = payload.get("data", r.data)
        r.turma_id = payload.get("turma_id", r.turma_id)

        db.session.commit()
        return r.to_dict(), 200

    @ns.doc("excluir_reserva")
    @ns.response(200, "Reserva removida com sucesso")
    @ns.response(404, "Reserva não encontrada")
    def delete(self, id):
        """
        Remove uma reserva pelo ID
        ---
        tags:
          - Reservas
        summary: Exclui uma reserva do banco de dados
        parameters:
          - in: path
            name: id
            required: true
            schema:
              type: integer
        responses:
          200:
            description: Reserva removida com sucesso
          404:
            description: Reserva não encontrada
        """
        r = Reserva.query.get(id)
        if not r:
            return {"mensagem": "Reserva não encontrada"}, 404
        db.session.delete(r)
        db.session.commit()
        return {"mensagem": "Removida com sucesso"}, 200
