from flask import Flask, flash, session, request, redirect, render_template, url_for

from db.data_layer import create_project, get_all_projects, get_project, update_project, delete_project
from db.data_layer import create_task, get_all_tasks, get_task, update_task, delete_task

app = Flask(__name__)

@app.route('/')
def index():
    db_projects = get_all_projects()
    return render_template('index.html', projects=db_projects)

@app.route('/create_project', methods=['POST'])
def create_project_request():
    server_name = request.form['html_name']
    
    create_project(server_name)
    return redirect(url_for('index'))

@app.route('/edit_project/<project_id>')
def edit_project(project_id):
    db_project = get_project(project_id)
    return render_template('edit_project.html', project=db_project)

@app.route('/update_project', methods=['POST', 'GET'])
def update_project_request():
    project_id = request.form['html_id']
    project_name = request.form['html_name']
    update_project(project_id, project_name)
    return redirect(url_for('index'))

@app.route('/delete_project/<project_id>')
def delete_project_request(project_id):
    delete_project(project_id)
    return redirect(url_for('index'))

@app.route('/project/<project_id>')
def project_index(project_id):
    db_project = get_project(project_id)
    return render_template('project_index.html', project=db_project)

@app.route('/project/<project_id>/create_task', methods=['POST'])
def create_task_request(project_id):
    description = request.form['task_description']
    create_task(project_id, description)
    return redirect(url_for('project_index', project_id = project_id))

@app.route('/project/<project_id>/edit_task/<task_id>')
def edit_task(project_id, task_id):
    db_task = get_task(task_id)
    return render_template('edit_task.html', task = db_task)

@app.route('/update_task', methods=['POST', 'GET'])
def update_task_request():
    task_id = request.form['task_id']
    description = request.form['task_description']
    project_id = request.form['project_id']
    update_task(task_id, description)
    return redirect(url_for('project_index', project_id = project_id))

@app.route('/delete_task/<task_id>')
def delete_task_request(task_id):
    task = get_task(task_id)
    project_id = task.project_id
    delete_task(task_id)
    return redirect(url_for('project_index', project_id = project_id))

app.run(debug=True)