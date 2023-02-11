from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin

#this is a decorator which will reload the user with the help of the id that is stored in the session and login manager is something that will be maintaining our all sessions at the backend
#so this extension is going to accept that our user model should have certain attributes like is_authenticated, is_active, is_anonymous, get_id and these things are so common that flask has already added them and we just have to import them (usermixins)
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
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