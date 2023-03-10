import os
import secrets
from PIL import Image
from flask import render_template, request, redirect, flash, url_for, request, abort
from werkzeug.utils import secure_filename
from flaskblog import app, bcrypt,db
from flaskblog.forms import RegistrationForm, LoginForm, AccountUpdateForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
  page = request.args.get('page', 1, type=int) #this is to get the page from the user and if he doesn't give this then we will be directly giving it as 1 and also metions the type
  posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=1) #this is a paginate request and here we are setting teh different pages according to the requests and also along with that we are arranging all the new posts first and the old ones after that
  title = "flask project"
  return render_template ('home.html', title=title, posts=posts)

@app.errorhandler(401)
def error_handling(error): #here the error is equal to the one which we assigned above but suppose we got different error than this we will not be able to run the page 
  return render_template('page_not_found.html'), 401


@app.route("/register", methods=['POST','GET'])
def register_func():
  if current_user.is_authenticated:
    return redirect(url_for("home"))
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
  #here we are using the current_user which will be checking that if the current user which is accessing our website is authenticated then we will stop the user to go to the login and the resgister page so same thing is used for the register.
  if current_user.is_authenticated:
    return redirect(url_for("home"))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      #this login_user will help us to login user after checking the username and the password that whether they are correct or not
      login_user(user, remember = form.remember.data)
      next_page = request.args.get("next")
      return redirect(next_page) if next_page else redirect(url_for('home')) #ternary condition
    else: 
      flash('Login unsuccessful, please check username and password!!', 'warning')
  return render_template ("login.html", title="Login page", form=form)

@app.route('/logout')
def logout_func():
  logout_user()
  return redirect(url_for("home"))

def save_picture(form_pic): #will help to save the picture uploaded by them with the hashed name
  hashed_name = secrets.token_hex(8)
  _, file_ext = os.path.splitext(form_pic.filename)
  picture_fn = hashed_name + file_ext
  picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
  output_size = (125,125)
  i = Image.open(form_pic)
  i.resize(output_size)
  i.save(picture_path)
  return picture_fn


#this app will be returning the profile of the individual user
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = AccountUpdateForm()
  if form.validate_on_submit():
    if form.picture.data: #this part is taking the image input from the user and then passing that to our save image function which will be renaming it, saving it in our system.
      picture_name = save_picture(form.picture.data)
    current_user.image = picture_name #and here we are saving our image equal to the output given by the save picture function

    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash("Account has been updated", 'success')
    return redirect(url_for('account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
  image_file = url_for('static', filename = 'profile_pics/' + current_user.image)
  return render_template("account.html", title="Account", image_file=image_file, form=form)

#this is how we handle the files uploaded by the user here we cannot trust the user so to secure our system we are using the secure_filename provided by the werkzeug.utils to save our system from any forgery attack
# @app.route('/upload/', methods=['GET', 'POST'])
# def upload():
#   if request.method == "POST":
#     file = request.files['file_name']
#     file.save(f'flask_proj/uploads/{secure_filename(file.filename)}')

@app.route('/post/new/', methods=["GET", "POST"])
@login_required
def create_post():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(title = form.title.data, content = form.content.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    flash("Post has been created", 'success')
    return redirect (url_for("home"))
  return render_template('create_post.html', title="New Post", legend='Share Your Thoughts..', form=form)

@app.route("/post/<int:post_id>")
def post(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template("post.html", title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
def update_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.author != current_user:
    abort(403)
  form = PostForm()
  if form.validate_on_submit():
    post.title = form.title.data
    post.content = form.content.data
    db.session.commit()
    flash('Your post has been updated', 'success')
    return redirect(url_for('post', post_id=post.id))
  elif request.method == "GET":
    form.title.data = post.title
    form.content.data = post.content
  return render_template("create_post.html", title= f'Update {post.title}', legend='Update Post', form=form)

@app.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.author != current_user:
    abort(403)
  db.session.delete(post)
  db.session.commit()
  flash('Your post has been deleted', 'success')
  return redirect(url_for('home'))