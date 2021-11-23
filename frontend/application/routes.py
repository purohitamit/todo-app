from application import app
from flask import render_template, request, redirect, url_for, jsonify
from application.forms import TaskForm
import requests


@app.route('/')
@app.route('/home')
def home():
    all_tasks = request.get("http://todo-app-backend:5000/read/allTasks").json()
    return render_template('index.html', title = "Home", all_tasks=all_tasks["tasks"])


@app.route('/create/task', methods= ['GET', 'POST'])
def create_task():
    form = TaskForm()
    if request.method == "POST":
        response = requests.post("http://todo-app-backend:5000/create/task", json={"description": form.description.data} )
        return redirect(url_for('home'))
    return render_template("create_form.html", title = "Add a new task", form=form)



@app.route('/update/task/<int:id>', methods = ['GET', 'POST'])
def update_task(id):
    form = TaskForm()
    task = requests.get(f"http://todo-app-backend:5000/read/task/{id}")
    if request.method == "POST":
        response = requests.post(f"http://todo-app-backend:5000/create/task/{id}", json={"description": form.description.data} )
        return redirect(url_for('home'))

    return render_template("update_task.html", task=task, form=form, title = "Update")


@app.route('/delete/task/<int:id>')
def delete_task(id):
    task = Tasks.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/complete/task/<int:id>')
def complete_task(id):
    task = Tasks.query.get(id)
    task.completed = True
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/incomplete/task/<int:id>')
def incomplete_task(id):
    task = Tasks.query.get(id)
    task.completed = False
    db.session.commit()
    return redirect(url_for('home'))

