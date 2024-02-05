# app/app.py

import subprocess
from flask import Flask
from flask_migrate import Migrate
# from flask_script import Manager
from flask_restx import Api
from flasgger import Swagger
from .extensions import db
from .routes.routes import register_route

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/smartlibrary'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # 啟動 pg_ctl
    start_pg_ctl()

    # 初始化 Flask-Migrate
    migrate = Migrate(app, db)

    db.init_app(app)

    api = Api(app, version='1.0', title='Smart Library API', description='Smart Library API Documentation')
    swagger = Swagger()
    swagger.init_app(app)   
    
    register = register_route()
    register.register_books_routes(api)
    register.register_questionnaire_books_interest_routes(api)
    register.register_users_routes(api)
    register.register_authors_routes(api)
    register.register_ratings_routes(api)
    register.register_questionnaire_users_interest_routes(api)


    # @app.route('/')
    # def index():
    #     return 'Hello, Smart Library API!'

    return app
def start_pg_ctl():
    # 在這裡執行啟動 pg_ctl 的指令
    subprocess.run(['pg_ctl', 'restart', '-D', 'C:\Users\User\Documents\GitHub\smartlibraryAPI\smartlibrary_\SmartLibraryAPI\app\data'])
if __name__ == '__main__':
    create_app().run(debug=True)
