from flask import Flask
from flask_restx import Api
from config import Config
from models.reserva_model import db
from controller.routes import ns as reservas_ns
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Garante que a variável exista no config
    app.config["GERENCIAMENTO_BASE_URL"] = os.environ.get("GERENCIAMENTO_BASE_URL", "http://localhost:5000")

    db.init_app(app)

    api = Api(app, title="Reservas API", version="1.0", description="Serviço de Reservas")
    api.add_namespace(reservas_ns, path="/api/reservas")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
