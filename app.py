"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretkey'

connect_db(app)

with app.app_context():
  db.create_all()

@app.route('/')
def home():
  """Homepage"""
  return redirect("/user/list")

@app.route("/user/list")
def users_list():
  """show page with all user info"""
  
  user_list = User.query.order_by(User.first_name, User.last_name).all()
  return render_template('user_list.html', user_list = user_list)

@app.route("/user/new", methods = ["GET"])
def new_user():
  """create form for registering new user"""
  return render_template("user_new.html")

@app.route("/user/new", methods = ["POST"])
def register_user():
  """register new user"""
  user = User(
    first_name = request.form["first-name"],
    last_name = request.form["last-name"],
    image = request.form["image"] or None)
  db.session.add(user)
  db.session.commit()

  return redirect("/user/list")

@app.route("/user/<int:id>")
def user_details(id):
  """page of information on user"""

  user = User.query.get_or_404(id)
  return render_template("user_details.html", user = user)

@app.route("/user/edit/<int:id>", methods = ["GET"])
def edit_show(id):
  """change the information of a user"""

  user = User.query.get_or_404(id)
  return render_template("user_edit.html", user = user)

@app.route("/user/edit/<int:id>", methods = ["POST"])
def edit_user(id):
  """change the information of a user"""

  user = User.query.get_or_404(id)
  user.first_name = request.form["first-name"]
  user.last_name = request.form["last-name"]
  user.image = request.form["image"]

  db.session.add(user)
  db.session.commit()

  return redirect("/user/list")

@app.route("/user/remove/<int:id>", methods = ["POST"])
def remove_user(id):
  """remove a user from the database"""
  user = User.query.get_or_404(id)
  db.session.delete(user)
  db.session.commit()

  return redirect("/user/list")