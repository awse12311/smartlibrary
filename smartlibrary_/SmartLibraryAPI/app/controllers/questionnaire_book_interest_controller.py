# controllers/questionnaire_book_interest_controller.py
from flask import request
from flask_restx import Namespace, Resource, fields
from ..services.questionnaire_book_interest_service import questionnaire_book_interest_service
from ..models.questionnaire_users_interest import QuestionnaireUsersInterest

# 建立 Namespace
questionnaire_books_interest_namespace = Namespace('questionnaire_books_interest', description='Questionnaire Books Interest related operations')

# 資料模型
interest_model = questionnaire_books_interest_namespace.model('Interest', {
    'id': fields.Integer(readonly=True,description='Interest ID'),
    'parent_interest_id': fields.Integer(description='Parent Interest ID'),
    'interest_name': fields.String(required=True, description='Interest name'),
    'created_at': fields.String(description='Created at timestamp'),
    'updated_at': fields.String(description='Updated at timestamp'),
})

@questionnaire_books_interest_namespace.route('/')
class QuestionnaireBooksInterestResource(Resource):
    @questionnaire_books_interest_namespace.expect(interest_model)
    def post(self):
        """Create a new interest"""
        try:
            data = request.get_json()
            interest = questionnaire_book_interest_service.create_interest(data)
            return (interest.serialize()), 201
        except Exception as e:
            return ({'error': str(e)}), 500

    def get(self):
        """Get all interests"""
        try:
            interests = questionnaire_book_interest_service.get_all_interests()
            return ([interest.serialize() for interest in interests]), 200
        except Exception as e:
            return ({'error': str(e)}), 500

@questionnaire_books_interest_namespace.route('/<int:id>')
class QuestionnaireBooksInterestDetailResource(Resource):
    def get(self, id):
        """Get interest by ID"""
        try:
            interest = questionnaire_book_interest_service.get_interest_by_id(id)
            if interest is None:
                return ({'error': 'Interest not found'}), 404
            return (interest.serialize()), 200
        except Exception as e:
            return ({'error': str(e)}), 500

    @questionnaire_books_interest_namespace.expect(interest_model)
    def put(self, id):
        """Update an interest"""
        try:
            data = request.get_json()
            interest = questionnaire_book_interest_service.update_interest(id, data)
            if interest is None:
                return ({'error': 'Interest not found'}), 404
            return (interest.serialize()), 200
        except Exception as e:
            return ({'error': str(e)}), 500

    def delete(self, id):
        """Delete an interest"""
        try:
            success, msg = questionnaire_book_interest_service.delete_interest(id)
            if not success:
                return ({'error': msg}), 404
            return ({'result': msg}), 200
        except Exception as e:
            return ({'error': str(e)}), 500



# # controllers/questionnaire_book_interest_controller.py
# from flask import Blueprint, request, jsonify
# from ..services.questionnaire_book_interest_service import questionnaire_book_interest_service

# questionnaire_books_interest_blueprint = Blueprint('questionnaire_books_interest', __name__, url_prefix='/api/questionnaire_books_interest')

# @questionnaire_books_interest_blueprint.route('/', methods=['POST'])
# def create_interest():
#     try:
#         data = request.get_json()
#         interest = questionnaire_book_interest_service.create_interest(data)
#         return jsonify(interest.serialize()), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @questionnaire_books_interest_blueprint.route('/', methods=['GET'])
# def get_interests():
#     try:
#         interests = questionnaire_book_interest_service.get_all_interests()
#         return jsonify([interest.serialize() for interest in interests]), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @questionnaire_books_interest_blueprint.route('/<int:id>', methods=['GET'])
# def get_interest(id):
#     try:
#         interest = questionnaire_book_interest_service.get_interest_by_id(id)
#         if interest is None:
#             return jsonify({'error': 'Interest not found'}), 404
#         return jsonify(interest.serialize()), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @questionnaire_books_interest_blueprint.route('/<int:id>', methods=['PUT'])
# def update_interest(id):
#     try:
#         data = request.get_json()
#         interest = questionnaire_book_interest_service.update_interest(id, data)
#         if interest is None:
#             return jsonify({'error': 'Interest not found'}), 404
#         return jsonify(interest.serialize()), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @questionnaire_books_interest_blueprint.route('/<int:id>', methods=['DELETE'])
# def delete_interest(id):
#     try:
#         success, msg = questionnaire_book_interest_service.delete_interest(id)
#         if not success:
#             return jsonify({'error': msg}), 404
#         return jsonify({'result': msg}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
