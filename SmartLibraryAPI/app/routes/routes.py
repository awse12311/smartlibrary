# routes/routes.py

# from flask import Blueprint
from flask_restx import Api
from ..controllers.books_controller import  books_namespace
from ..controllers.questionnaire_book_interest_controller import  questionnaire_books_interest_namespace
from ..controllers.users_controller import  users_namespace
from ..controllers.authors_controller import  authors_namespace
from ..controllers.ratings_controller import  ratings_namespace
from ..controllers.questionnaire_users_interest_controller import  qn_users_interests_namespace
# from ..controllers.camera_controller import  camera_namespace

class register_route:
    def register_books_routes(self,api):
        api.add_namespace(books_namespace, path='/api/books')

    def register_questionnaire_books_interest_routes(self,api):
        api.add_namespace(questionnaire_books_interest_namespace, path='/api/questionnaire_books_interest')
 
    def register_users_routes(self,api):
        api.add_namespace(users_namespace, path='/api/users')

    def register_authors_routes(self,api):
        api.add_namespace(authors_namespace, path='/api/authors')

    def register_ratings_routes(self,api):
        api.add_namespace(ratings_namespace, path='/api/ratings')

    def register_questionnaire_users_interest_routes(self,api):
        api.add_namespace(qn_users_interests_namespace, path='/api/questionnaire_users_interests')
    # def register_questionnaire_users_interest_routes(self,api):
    #     api.add_namespace(camera_namespace, path='/api/camera')



# # routes/routes.py

# from ..controllers.books_controller import books_blueprint
# from ..controllers.questionnaire_book_interest_controller import questionnaire_books_interest_blueprint
# from ..controllers.users_controller import users_blueprint
# from ..controllers.authors_controller import authors_blueprint
# from ..controllers.ratings_controller import ratings_blueprint
# from ..controllers.questionnaire_users_interest_controller import qn_users_interests_blueprint

# class register_route:
#     def register_books_routes(app):
#         app.register_blueprint(books_blueprint)
        
#     def register_questionnaire_books_interest_blueprint_routes(app):
#         app.register_blueprint(questionnaire_books_interest_blueprint)
        
#     def register_users_routes(app):
#         app.register_blueprint(users_blueprint)
        
#     def register_authors_routes(app):
#         app.register_blueprint(authors_blueprint)
        
#     def register_ratings_routes(app):
#         app.register_blueprint(ratings_blueprint)
        
#     def register_questionnaire_users_interest_routes(app):
#         app.register_blueprint(qn_users_interests_blueprint)
