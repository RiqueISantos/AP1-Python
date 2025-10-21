from flask_restx import fields

def reserva_model(ns):
    return ns.model('Reserva', {
        'num_sala': fields.Integer(required=True, description="Número da sala"),
        'lab': fields.Boolean(required=True, description="Se é laboratório"),
        'data': fields.String(required=True, description="Data da reserva"),
        'turma_id': fields.Integer(required=True, description="ID da turma")
    })
