from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import uuid

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI") # Set the connection string to connect to the database
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = str(uuid.uuid4())
db = SQLAlchemy(app)

from application import routes