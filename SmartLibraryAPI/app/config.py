# config.py

import os

class Config:
    # Flask app configuration
    SECRET_KEY = 'postgres'
    DEBUG = False

    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:smartlibrary@localhost/smartlibrary'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
