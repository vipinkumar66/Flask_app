from flask import render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
from flaskblog import app, bcrypt,db
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user

posts = [
  {
  'title':'Templates',
  'content':'They reduce the code size and make our application neat and clear',
  'author':'Vipin Kumar'
  },
  {
  'title':'Render_template',
  'content': 'Whenever we wanted to return the template for a particular url we have to use the render template function',
  'author':'Unknown'
  }
]



@app.route('/')
@app.route('/home')
def home():
  title = "flask project"
  return render_template ('home.html', title=title, posts=posts)

@app.errorhandler(401)
def error_handling(error): #here the error is equal to the one which we assigned above but suppose we got different error than this we will not be able to run the page 
  return render_template('page_not_found.html'), 401


@app.route("/register", methods=['POST','GET'])
def register_func():
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username = form.username.data, email=form.email.data, password = hashed_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Account created', 'success')
    return redirect(url_for('login_func'))
  return render_template('register.html', title = 'Registration Form', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_func():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      #this login_user will help us to login user after checking the username and the password that whether they are correct or not
      login_user(user, remember = form.remember.data)
      return redirect(url_for("home")) 
    flash('Login unsuccessful, please check username and password!!', 'warning')
  return render_template ("login.html", title="Login page", form=form)

#this is how we handle the files uploaded by the user here we cannot trust the user so to secure our system we are using the secure_filename provided by the werkzeug.utils to save our system from any forgery attack
@app.route('/upload/', methods=['GET', 'POST'])
def upload():
  if request.method == "POST":
    file = request.files['file_name']
    file.save(f'flask_proj/uploads/{secure_filename(file.filename)}')
