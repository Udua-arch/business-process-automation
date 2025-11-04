from flask import Flask, render_template, request, redirect
from models import db, Task
from rules import assign_task
from datetime import date
from datetime import datetime
from models import db, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.all()
    today = datetime.today().date()

    # Automatically update overdue tasks
    for task in tasks:
        if task.deadline and task.deadline < today and task.status.lower() != "completed":
            task.status = "Overdue"
    db.session.commit()

    # Count statuses
    completed_count = Task.query.filter(Task.status.ilike('completed')).count()
    progress_count = Task.query.filter(Task.status.ilike('in progress')).count()
    pending_count = Task.query.filter(Task.status.ilike('pending')).count()
    overdue_count = Task.query.filter(Task.status.ilike('overdue')).count()

    return render_template(
        'index.html',
        tasks=tasks,
        completed_count=completed_count,
        progress_count=progress_count,
        pending_count=pending_count,
        overdue_count=overdue_count
    )


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        deadline_str = request.form['deadline']
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()

        new_task = Task(title=title, amount=amount, deadline=deadline)
        new_task = assign_task(new_task)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    return render_template('add_task.html')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.status = "Completed"
        db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
