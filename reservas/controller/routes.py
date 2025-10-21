from flask import request
from flask_restx import Namespace, Resource
import requests
from models import db, Reserva
from models.schemas import reserva_model

ns = Namespace("reservas", description="Operações de reservas")

@ns.route("")
class ReservaList(Resource):
    @ns.doc("listar_reservas")
    def get(self):
        reservas = Reserva.query.all()
        return [r.to_dict() for r in reservas], 200

    @ns.expect(reserva_model(ns), validate=True)
    @ns.doc("criar_reserva")
    def post(self):
        payload = request.json
        turma_id = payload.get("turma_id")
        base = request.environ.get("GERENCIAMENTO_BASE_URL") or request.app.config["GERENCIAMENTO_BASE_URL"]
        resp = requests.get(f"{base}/turmas/{turma_id}")
        if resp.status_code == 404:
            return {"mensagem": f"Turma {turma_id} não encontrada no serviço de Gerenciamento"}, 400
        if resp.status_code >= 400:
            return {"mensagem": "Erro ao consultar serviço de Gerenciamento"}, 502

        r = Reserva(
            num_sala=payload.get("num_sala"),
            lab=payload.get("lab", False),
            data=payload["data"],
            turma_id=turma_id
        )
        db.session.add(r)
        db.session.commit()
        return r.to_dict(), 201

@ns.route("/<int:id>")
class ReservaResource(Resource):
    @ns.doc("obter_reserva")
    def get(self, id):
        r = Reserva.query.get(id)
        if not r:
            return {"mensagem": "Reserva não encontrada"}, 404
        return r.to_dict(), 200

    @ns.expect(reserva_model(ns), validate=True)
    @ns.doc("atualizar_reserva")
    def put(self, id):
        r = Reserva.query.get(id)
        if not r:
            return {"mensagem": "Reserva não encontrada"}, 404
        payload = request.json
        r.num_sala = payload.get("num_sala", r.num_sala)
        r.lab = payload.get("lab", r.lab)
        r.data = payload.get("data", r.data)
        new_turma = payload.get("turma_id")
        if new_turma and new_turma != r.turma_id:
            base = request.app.config["GERENCIAMENTO_BASE_URL"]
            resp = requests.get(f"{base}/turmas/{new_turma}")
            if resp.status_code == 404:
                return {"mensagem": f"Turma {new_turma} não encontrada no serviço de Gerenciamento"}, 400
            if resp.status_code >= 400:
                return {"mensagem": "Erro ao consultar serviço de Gerenciamento"}, 502
            r.turma_id = new_turma

        db.session.commit()
        return r.to_dict(), 200

    @ns.doc("excluir_reserva")
    def delete(self, id):
        r = Reserva.query.get(id)
        if not r:
            return {"mensagem": "Reserva não encontrada"}, 404
        db.session.delete(r)
        db.session.commit()
        return {"mensagem": "Removida com sucesso"}, 200
