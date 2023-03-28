from flask import Flask, redirect, url_for, render_template, request, session, flash
from models import db, ToDo, User


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
    email = session.get("user_email")
    user = User.query.filter(User.email == email).first()

    return render_template('home.html',email = email, user = user)


@app.route('/user/<user_id>')
def user_page(user_id):
    email = session.get("user_email")
    user = User.query.filter(User.email == email).first()
    todo_list = ToDo.query.filter(ToDo.user_id == user_id)
    return render_template('user.html', todo_list=todo_list, user = user,user_id= user_id)


@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('name')
    user_id = request.form.get('user_id')
    due_date = request.form.get('due_date')

    new_task = ToDo(task=task, due_date=due_date, user_id = user_id)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/user/<user_id>')


@app.route('/update/<todo_id>')
def update(todo_id):
    todo = ToDo.query.get(todo_id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect('/')


@app.route('/delete/<todo_id>')
def delete(todo_id):
    todo = ToDo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@ app.route('/create_account')
def create_account_page():
    return render_template("create_account.html")


@ app.route("/users", methods=["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter(User.email == email).first()
    if user:
        flash(
            "Account with that email already exists. Please log in or try a different email")
        return redirect('/create_account')
    else:
        user = User(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    return redirect('/')


@ app.route("/login", methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter(User.email == email).first()

    if not user or user.password != password:
        flash("The email or password you entered was incorrect")
    else:
        session['user_email'] = user.email
        flash(f"Welcome Back,{user.email}!")
    return redirect('/')

@ app.route("/logout")
def logout():
    del session['user_email']
    session["cart"] = {}
    flash("You're logged out")
    return redirect("/")


if __name__ == "__main__":
    app.run(port=3000)
