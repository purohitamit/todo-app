from flask.templating import render_template
from application import app, db
from application.models import Tasks
from flask import render_template, request, redirect, url_for
from application.forms import TaskForm


@app.route('/')
@app.route('/home')
def home():
    all_tasks = Tasks.query.all()
    return render_template('index.html', title = "home", all_tasks=all_tasks)

@app.route('/create/task', methods= ['GET', 'POST'])
def create_task():
    form = TaskForm()
    if request.method == "POST":
        new_task = Tasks(description=form.description.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("create_form.html", title = "Add a new task", form=form)

@app.route('/read/allTasks')
def read_tasks():
    all_tasks = Tasks.query.all()
    
    tasks_dict = {"tasks": []}
    
    for task in all_tasks:
        tasks_dict ["tasks"].append(
            {
                "description": task.description, 
                "completed": task.completed}
            )
    return tasks_dict

@app.route('/update/task/<int:id>/<new_description>')
def update_task(id, new_description):
    task = Tasks.query.get(id)
    task.description = new_description
    db.session.commit()
    return f'task{id} updated to {new_description}'


@app.route('/delete/task/<int:id>')
def delete_task(id):
    task = Tasks.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return f'task{id} is deleted now.'

@app.route('/complete/task/<int:id>')
def complete_task(id):
    task = Tasks.query.get(id)
    task.completed = True
    db.session.commit()
    return f'task{id} is completed'

@app.route('/incomplete/task/<int:id>')
def incomplete_task(id):
    task = Tasks.query.get(id)
    task.completed = False
    db.session.commit()
    return f'task{id} is not completed'

