from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__) #here we are creating an instance of our Flask application and the __name__ basically tells the application that where it should look for the resources
app.config['SECRET_KEY'] = "e065411bfdc873275a5d6dc65724c4e1"
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///site.db" 
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from flaskblog import routes

 #this is written here to avoid the circular import error and also so that our application can find our routes because our run file is going to import app from here only and this is basically initalizing part of our application