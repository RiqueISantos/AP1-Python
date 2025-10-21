from flask_restx import fields, Model

def reserva_model(ns):
    return ns.model("Reserva", {
        "id": fields.Integer(readonly=True),
        "num_sala": fields.Integer(required=False, description="Número da sala"),
        "lab": fields.Boolean(required=False, description="É laboratório?"),
        "data": fields.String(required=True, description="Data em formato YYYY-MM-DD"),
        "turma_id": fields.Integer(required=True, description="ID da turma (do serviço Gerenciamento)")
    })
