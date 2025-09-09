from flask import request, render_template, redirect, url_for, flash
from models.professor_model import Professor
from models.aluno_model import Aluno
from models.turma_model import Turma
from models.database import db
from datetime import datetime

def setup_routes(app):

    # ----- CRUD Professor -----
    @app.route('/professores', methods=['GET', 'POST'])
    def professores():
        if request.method == 'POST':
            professor = Professor(
                nome=request.form['nome'],
                idade=int(request.form['idade']),
                materia=request.form['materia'],
                observacoes=request.form.get('observacoes', '')
            )
            db.session.add(professor)
            db.session.commit()
            flash("Professor adicionado!")
            return redirect(url_for('professores'))
        
        professores = Professor.query.all()
        return render_template('index.html', professores=professores)

    @app.route('/professores/update/<int:id>', methods=['POST'])
    def update_professor(id):
        professor = Professor.query.get_or_404(id)
        professor.nome = request.form['nome']
        professor.idade = int(request.form['idade'])
        professor.materia = request.form['materia']
        professor.observacoes = request.form.get('observacoes', '')
        db.session.commit()
        flash("Professor atualizado!")
        return redirect(url_for('professores'))

    @app.route('/professores/delete/<int:id>', methods=['POST'])
    def delete_professor(id):
        professor = Professor.query.get_or_404(id)
        db.session.delete(professor)
        db.session.commit()
        flash("Professor deletado!")
        return redirect(url_for('professores'))


    # ----- CRUD Turma -----
    @app.route('/turmas', methods=['GET', 'POST'])
    def turmas():
        if request.method == 'POST':
            turma = Turma(
                descricao=request.form['descricao'],
                professor_id=int(request.form['professor_id']),
                ativo=True if request.form.get('ativo') == 'true' else False
            )
            db.session.add(turma)
            db.session.commit()
            flash("Turma adicionada!")
            return redirect(url_for('turmas'))

        turmas = Turma.query.all()
        professores = Professor.query.all()
        return render_template('index.html', turmas=turmas, professores=professores)

    @app.route('/turmas/update/<int:id>', methods=['POST'])
    def update_turma(id):
        turma = Turma.query.get_or_404(id)
        turma.descricao = request.form['descricao']
        turma.professor_id = int(request.form['professor_id'])
        turma.ativo = True if request.form.get('ativo') == 'true' else False
        db.session.commit()
        flash("Turma atualizada!")
        return redirect(url_for('turmas'))

    @app.route('/turmas/delete/<int:id>', methods=['POST'])
    def delete_turma(id):
        turma = Turma.query.get_or_404(id)
        db.session.delete(turma)
        db.session.commit()
        flash("Turma deletada!")
        return redirect(url_for('turmas'))


    # ----- CRUD Aluno -----
    @app.route('/alunos', methods=['GET', 'POST'])
    def alunos():
        if request.method == 'POST':
            data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d').date()
            aluno = Aluno(
                nome=request.form['nome'],
                idade=int(request.form['idade']),
                turma_id=int(request.form['turma_id']),
                data_nascimento=data_nascimento,
                nota_primeiro_semestre=float(request.form['nota_primeiro_semestre']),
                nota_segundo_semestre=float(request.form['nota_segundo_semestre']),
                media_final=float(request.form['media_final'])
            )
            db.session.add(aluno)
            db.session.commit()
            flash("Aluno adicionado!")
            return redirect(url_for('alunos'))

        alunos = Aluno.query.all()
        turmas = Turma.query.all()
        return render_template('index.html', alunos=alunos, turmas=turmas)

    @app.route('/alunos/update/<int:id>', methods=['POST'])
    def update_aluno(id):
        aluno = Aluno.query.get_or_404(id)
        aluno.nome = request.form['nome']
        aluno.idade = int(request.form['idade'])
        aluno.turma_id = int(request.form['turma_id'])
        aluno.data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d').date()
        aluno.nota_primeiro_semestre = float(request.form['nota_primeiro_semestre'])
        aluno.nota_segundo_semestre = float(request.form['nota_segundo_semestre'])
        aluno.media_final = float(request.form['media_final'])
        db.session.commit()
        flash("Aluno atualizado!")
        return redirect(url_for('alunos'))

    @app.route('/alunos/delete/<int:id>', methods=['POST'])
    def delete_aluno(id):
        aluno = Aluno.query.get_or_404(id)
        db.session.delete(aluno)
        db.session.commit()
        flash("Aluno deletado!")
        return redirect(url_for('alunos'))
