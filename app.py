"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag

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
  posts = Post.query.order_by(Post.created_at.desc()).limit(10).all()
  return render_template("homepage.html", posts = posts)
  # return redirect("/user/list")

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
  posts = Post.query.filter_by(user_id = user.id).order_by(Post.created_at.desc()).limit(5)
  return render_template("user_details.html", user = user, posts = posts)

@app.route("/user/<int:id>/posts")
def user_posts(id):
  """page of posts related to given user"""

  user = User.query.get_or_404(id)
  posts = Post.query.filter_by(user_id = user.id).order_by(Post.created_at.desc())
  return render_template("user_posts.html", user = user, posts = posts)

@app.route("/user/<int:id>/posts/new", methods = ["GET", "POST"])
def new_post(id):
  """page with form for creating a new post"""

  user = User.query.get_or_404(id)
  tags = Tag.query.all()
  if request.method == "POST":
    tag_ids = [int(num) for num in request.form.getlist("tag")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post(
      title = request.form["title"],
      content = request.form["content"],
      user_id = id)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/user/{ id }")
  
  return render_template("user_post.html", user = user, tags = tags)

@app.route("/post/<int:id>", methods = ["GET"])
def post(id):
  """post details"""
  post = Post.query.get_or_404(id)
  return render_template("post.html", post = post)

@app.route("/post/<int:id>/edit", methods = ["GET", "POST"])
def post_edit(id):
  """edit a post"""
  post = Post.query.get_or_404(id)
  tags = Tag.query.all()
  if request.method == "POST":
    post.title = request.form["title"]
    post.content = request.form["content"]

    tag_ids = [int(num) for num in request.form.getlist("tag")]
    post.tag = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    return redirect(f"/post/{ id }")
  else:
    return render_template("post_edit.html", post = post, tags = tags)

@app.route("/post/<int:id>/remove", methods = ["GET", "POST"])
def post_remove(id):
  """remove a post"""
  post = Post.query.get_or_404(id)
  if request.method == "POST":
    db.session.delete(post)
    db.session.commit()

    return redirect("/")
  else:
    return render_template("post_remove.html", post = post)


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

@app.route('/tag')
def tags_page():
  """show a page with an index of tags"""

  tags = Tag.query.all()
  return render_template('tags_page.html', tags = tags)

@app.route('/tag/new', methods = ["GET", "POST"])
def tag_new():
  """show form for making new tag and handle form submission"""

  posts = Post.query.all()
  if request.method == "POST":
    post_ids = [int(num) for num in request.form.getlist("post")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name = request.form['name'], post = posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tag')
  else:
    return render_template('tag_new.html', posts = posts)

@app.route('/tag/<int:id>')
def tag_details(id):
  """show a details page for a certain tag"""

  tag = Tag.query.get_or_404(id)
  return render_template('tag_details.html', tag = tag)

@app.route('/tag/<int:id>/edit', methods = ["GET", "POST"])
def tag_edit(id):
  """Show form for editing tag and handle form submission"""
  tag = Tag.query.get_or_404(id)
  if request.method == "POST":
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("post")]
    tag.post = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    return redirect(f"/tag/{ id }")
  else:
    posts = Post.query.all()
    return render_template("tag_edit.html", tag = tag, posts = posts)
  
@app.route('/tag/<int:id>/remove', methods = ["POST"])
def tag_remove(id):
  """handle tag deletion submission"""

  tag = Tag.query.get_or_404(id)
  db.session.delete(tag)
  db.session.commit()

  return redirect('/tag')