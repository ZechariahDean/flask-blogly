"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DEFAULT_IMAGE = "https://cdn.pixabay.com/photo/2021/07/02/04/48/user-6380868_640.png"

class User(db.Model):
  """blogly user."""

  __tablename__ = "user"

  id = db.Column(db.Integer, primary_key = True)
  first_name = db.Column(db.Text, nullable = False)
  last_name = db.Column(db.Text, nullable = False)
  image = db.Column(db.Text, nullable = False, default = DEFAULT_IMAGE)

  @property
  def get_name(self):
    """Return users full name"""

    return f"{self.first_name} {self.last_name}"

def connect_db(app):
  """Connect the database to application"""

  db.app = app
  db.init_app(app)