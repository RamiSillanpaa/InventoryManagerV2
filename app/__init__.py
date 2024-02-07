# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../varastonhallinta.db'

    db.init_app(app)

    from app.views import main
    app.register_blueprint(main)

    return app

