from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

# Database configuration
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
current_dir = os.path.dirname(os.path.abspath(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(current_dir, "nyt_strands.db")
db = SQLAlchemy(app)

# Login configuration
login_manager = LoginManager()
login_manager.init_app(app)

from app import routes