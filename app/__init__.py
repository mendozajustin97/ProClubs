from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager
from config import Config

# Create a Flask Instance
app = Flask(__name__)

# Add Database
app.config.from_object(Config)

# Initialize
db = SQLAlchemy(app)

migrate = Migrate(app,db)

login = LoginManager(app)

login.login_view = 'login'

from . import routes

@app.before_first_request
def create_tables():
    db.create_all()