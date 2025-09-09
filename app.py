from flask import Flask, render_template
from flasgger import Swagger
from models.professor_model import Professor
from models.turma_model import Turma
from models.aluno_model import Aluno
from controller.route import setup_routes
from models.database import db

app = Flask(__name__)
app.secret_key = 'projeto-API' 
swagger = Swagger(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
setup_routes(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    professores = Professor.query.all()
    turmas = Turma.query.all()
    alunos = Aluno.query.all()
    return render_template('index.html', professores=professores, turmas=turmas, alunos=alunos)


if __name__ == '__main__':
    app.run(debug=True)
