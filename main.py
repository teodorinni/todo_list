import sqlite3
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

# create db
# db = sqlite3.connect("todo_list.db")
# cursor = db.cursor()
# cursor.execute("CREATE TABLE list (id INTEGER PRIMARY KEY, content varchar(250) NOT NULL DEFAULT 0,
# status INTEGER NOT NULL DEFAULT 0, editable INTEGER NOT NULL)")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo_list.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    editable = db.Column(db.Integer, nullable=False, default=0)


@app.route("/", methods=["GET", "POST"])
def index():
    all_tasks = db.session.query(List).all()
    if len(all_tasks) > 0:
        new_task_id = all_tasks[len(all_tasks)-1].id + 1
        return render_template("index.html", tasks=all_tasks, new_task_id=new_task_id)
    else:
        return render_template("index.html", tasks="none", new_task_id=1)


@app.route("/done/<int:task_id>")
def done(task_id):
    task = List.query.get(task_id)
    task.status = 1
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/not_done/<int:task_id>")
def not_done(task_id):
    task = List.query.get(task_id)
    task.status = 0
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = List.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/add", methods=["POST"])
def add():
    new_task = List()
    new_task.content = request.form["content"]
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/edit/<int:task_id>")
def edit(task_id):
    task = List.query.get(task_id)
    task.editable = 1
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/save/<int:task_id>", methods=["POST"])
def save(task_id):
    task = List.query.get(task_id)
    task.content = request.form["content"]
    task.editable = 0
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
