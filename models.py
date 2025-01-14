"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
DEFAULT_IMAGE = "https://cdn.pixabay.com/photo/2021/07/02/04/48/user-6380868_640.png"

class User(db.Model):
  """blogly user."""

  __tablename__ = "user"

  id = db.Column(db.Integer, primary_key = True)
  first_name = db.Column(db.Text, nullable = False)
  last_name = db.Column(db.Text, nullable = False)
  image = db.Column(db.Text, nullable = False, default = DEFAULT_IMAGE)

  posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

  @property
  def get_name(self):
    """Return users full name"""

    return f"{self.first_name} {self.last_name}"

class Post(db.Model):
  """blogly post"""

  __tablename__ = "post"

  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.Text, nullable = False)
  content = db.Column(db.Text, nullable = True)
  created_at = db.Column(db.DateTime, nullable = False, default = datetime.now())
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

  @property
  def format_date(self):
    """Return formatted date."""

    return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

class PostTag(db.Model):
  """m2m between tag and post"""

  __tablename__ = "posttag"

  post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False, primary_key = True)
  tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable = False, primary_key = True)

class Tag(db.Model):
  """blogly tag"""

  __tablename__ = "tag"

  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.Text, nullable = False, unique = True)

  post = db.relationship(
    'Post',
    secondary = "posttag",
    backref = "tag",
  )

def connect_db(app):
  """Connect the database to application"""
  db.app = app
  db.init_app(app)
