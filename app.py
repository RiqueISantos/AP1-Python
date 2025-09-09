import os
from flask import Flask
from config import Config
from models import db

app = Flask(__name__, template_folder=os.path.join('view', 'templates'))
app.config.from_object(Config)

# inicializa o banco de dados
db.init_app(app)

# cria tabelas
with app.app_context():
    db.create_all()



if __name__ == '__main__':
    app.run(debug=True, port=5002)
