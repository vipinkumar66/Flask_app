from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__) #here we are creating an instance of our Flask application and the __name__ basically tells the application that where it should look for the resources
app.config['SECRET_KEY'] = os.getenv("flask_secret_key")
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///site.db" 
db = SQLAlchemy(app)
'''THE USER AUTHENTICATION PART'''
bcrypt = Bcrypt(app) #this is important for hashing the password and then storing them
login_manager = LoginManager(app) #this is going to manage all our sessions at the backend
login_manager.login_view = "login_func" #this part is done for our login_required decorator to tell him okay if any page of the website which requires login_required then where he should go, so he should go to the login page
login_manager.login_message_category = "info"
from flaskblog import routes

 #this is written here to avoid the circular import error and also so that our application can find our routes because our run file is going to import app from here only and this is basically initalizing part of our application