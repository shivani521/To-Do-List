from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def home():
    todo_list = Todo.query.all()
    flashed_messages = get_flashed_messages(with_categories=True)
    return render_template("base.html", todo_list=todo_list, flashed_messages=flashed_messages)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")

    if not title:
        flash('Please enter a non-blank item.', 'warning')
    else:
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()

    return redirect(url_for("home"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo_to_delete = Todo.query.get(todo_id)
    
    if todo_to_delete:
        db.session.delete(todo_to_delete)
        db.session.commit()

        update_task_indices()

    return redirect(url_for("home"))

def update_task_indices():
    remaining_tasks = Todo.query.all()

    for index, task in enumerate(remaining_tasks, start=1):
        task.id = index

    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)