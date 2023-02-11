from flaskblog import db
from datetime import datetime

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(20), nullable = False, unique = True)
  email = db.Column(db.String(120), nullable = False, unique = True)
  image = db.Column(db.String(20), nullable = False, default='default.jpg')
  password = db.Column(db.String(60), nullable=False)
  posts = db.relationship('Post', backref = 'author', lazy=True)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}','{self.image}')"


class Post(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(100), nullable = False)
  content = db.Column(db.Text, nullable = False)
  image = db.Column(db.String(30))
  date_posted = db.Column(db.DateTime, nullable=False, default = datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __repr__(self):
    return f"Post('{self.title}', '{self.date_posted}')"