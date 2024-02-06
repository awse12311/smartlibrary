# app/__init__.py
from flask import Flask
from app import controllers
from app.controllers import bp
from app import models, controllers

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    

    return app

# from flask_sqlalchemy import SQLAlchemy

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mynonsuperuser:your_password@localhost/myinner_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)