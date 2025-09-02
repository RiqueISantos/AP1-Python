from flask import render_template, request, redirect, url_for
from models import db
from models.task import Task
from models.user import User

class TaskController:

    @staticmethod
    def list_tasks():
        # TODO buscar todas as tarefas do banco de dados
        tasks = None 
        return render_template("tasks.html", tasks=tasks)

    @staticmethod
    def create_task():
        
        if request.method == "POST":
            
            # TODO capturar dados do formulário (title, description, user_id)
            # TODO criar um novo objeto Task com os dados capturados
            # TODO adicionar no db.session e dar commit
            pass

            return redirect(url_for("list_tasks"))

        # TODO buscar todos os usuários para exibir no <select> do formulário
        users = None
        return render_template("create_task.html", users=users)
    
    @staticmethod
    def update_task_status(task_id):
        # TODO buscar a tarefa pelo id
        # TODO: se existir, alternar status entre "Pendente" e "Concluído" e dar commit na alteração
        pass 

        return redirect(url_for("list_tasks"))

    @staticmethod
    def delete_task(task_id):
        
        # TODO buscar a tarefa pelo id
        # TODO: se ela existir, remover do db.session e dar commit
        pass 
    
        return redirect(url_for("list_tasks"))