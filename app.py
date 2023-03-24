from flask import Flask, redirect, url_for, render_template, request
from models import db
import sqlite3

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)

db.create_all()


@app.route("/")
def index():
 
    return render_template('home.html')


@app.route('/user/<user_id>')
def user_page(user_id):
    return render_template('user.html')


@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')

    new_task = ToDo(name=name)


if __name__ == "__main__":
    app.run(port=3000)
