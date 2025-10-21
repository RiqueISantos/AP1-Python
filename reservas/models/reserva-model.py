from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Reserva(db.Model):
    __tablename__ = "reservas"

    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.Integer, nullable=True)
    lab = db.Column(db.Boolean, default=False)
    data = db.Column(db.String(10), nullable=False) 
    turma_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "num_sala": self.num_sala,
            "lab": self.lab,
            "data": self.data,
            "turma_id": self.turma_id
        }
