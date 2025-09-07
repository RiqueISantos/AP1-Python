from models import db

class Task(db.Model):
    __tablename__ = "tasks"

    # TODO: Define os campos e o relacionamento da tabela Task
    # - id: chave primária da tarefa
    # - title: título da tarefa (obrigatório)
    # - description: descrição detalhada da tarefa (obrigatório)
    # - user_id: chave estrangeira que conecta a tarefa a um usuário (não nulo)
    # - status: indica o estado da tarefa, padrão "Pendente"
    # - user: relacionamento com a classe User, usando back_populates="tasks" para criar o vínculo bidirecional

    def __repr__(self):
        return f"<Task {self.title} - {self.status}>"
