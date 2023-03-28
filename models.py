from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, email, password):
        self.email = email
        self.password = password


class ToDo(db.Model):
    __tablename__ = 'to_dos'

    todo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    task = db.Column(db.String)
    due_date = db.Column(db.String)
    completed = db.Column(db.Boolean)

    user = db.relationship('User', backref='to_dos')

    def __init__(self, user_id, task, due_date):
        self.user_id = user_id
        self.task = task
        self.due_date = due_date
        self.completed = False
