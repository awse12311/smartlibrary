# controllers/questionnaire_users_interest_controller.py
from flask import request
from flask_restx import Namespace, Resource, fields
from flask import jsonify
from ..services.questionnaire_users_interest_service import QuestionnaireUsersInterestService

# 建立 Namespace
qn_users_interests_namespace = Namespace('questionnaire_users_interests', description='Questionnaire Users Interests related operations')

# 資料模型
qn_users_interest_model = qn_users_interests_namespace.model('QuestionnaireUsersInterest', {
    'id': fields.Integer(readonly=True,description='Questionnaire Users Interest ID'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'interests_id': fields.Integer(description='Interests ID'),
    'created_at': fields.String(description='Created at timestamp'),
    'updated_at': fields.String(description='Updated at timestamp'),
})

@qn_users_interests_namespace.route('/')
class QuestionnaireUsersInterestResource(Resource):
    @qn_users_interests_namespace.expect(qn_users_interest_model)
    def post(self):
        """Create a new questionnaire users interest"""
        try:
            data = request.get_json()
            qn_users_interest = QuestionnaireUsersInterestService.create_questionnaire_users_interest(data)
            return (qn_users_interest.serialize()), 201
        except Exception as e:
            return ({'error': str(e)}), 500

    def get(self):
        """Get all questionnaire users interests"""
        try:
            qn_users_interests = QuestionnaireUsersInterestService.get_all_questionnaire_users_interests()
            return ([qi.serialize() for qi in qn_users_interests]), 200
        except Exception as e:
            return ({'error': str(e)}), 500

@qn_users_interests_namespace.route('/<int:qn_users_interest_id>')
class QuestionnaireUsersInterestDetailResource(Resource):
    def get(self, qn_users_interest_id):
        """Get questionnaire users interest by ID"""
        try:
            qn_users_interest = QuestionnaireUsersInterestService.get_questionnaire_users_interest_by_id(qn_users_interest_id)
            if qn_users_interest is None:
                return ({'error': 'Questionnaire Users Interest not found'}), 404
            return (qn_users_interest.serialize()), 200
        except Exception as e:
            return ({'error': str(e)}), 500

    @qn_users_interests_namespace.expect(qn_users_interest_model)
    def put(self, qn_users_interest_id):
        """Update a questionnaire users interest"""
        try:
            data = request.get_json()
            qn_users_interest = QuestionnaireUsersInterestService.update_questionnaire_users_interest(qn_users_interest_id, data)
            if qn_users_interest is None:
                return ({'error': 'Questionnaire Users Interest not found'}), 404
            return (qn_users_interest.serialize()), 200
        except Exception as e:
            return ({'error': str(e)}), 500

    def delete(self, qn_users_interest_id):
        """Delete a questionnaire users interest"""
        try:
            success = QuestionnaireUsersInterestService.delete_questionnaire_users_interest(qn_users_interest_id)
            if not success:
                return ({'error': 'Questionnaire Users Interest not found'}), 404
            return ({'result': 'Questionnaire Users Interest deleted'}), 200
        except Exception as e:
            return ({'error': str(e)}), 500




# from flask import Blueprint, request, jsonify
# from ..services.questionnaire_users_interest_service import QuestionnaireUsersInterestService

# qn_users_interests_blueprint = Blueprint('questionnaire_users_interests', __name__, url_prefix='/api/questionnaire_users_interests')

# @qn_users_interests_blueprint.route('/', methods=['POST'])
# def create_questionnaire_users_interest():
#     try:
#         data = request.get_json()
#         questionnaire_users_interest = QuestionnaireUsersInterestService.create_questionnaire_users_interest(data)
#         return jsonify(questionnaire_users_interest.serialize()), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @qn_users_interests_blueprint.route('/', methods=['GET'])
# def get_questionnaire_users_interests():
#     try:
#         questionnaire_users_interests = QuestionnaireUsersInterestService.get_all_questionnaire_users_interests()
#         return jsonify([qi.serialize() for qi in questionnaire_users_interests]), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @qn_users_interests_blueprint.route('/<int:qn_users_interest_id>', methods=['GET'])
# def get_questionnaire_users_interest(qn_users_interest_id):
#     try:
#         questionnaire_users_interest = QuestionnaireUsersInterestService.get_questionnaire_users_interest_by_id(qn_users_interest_id)
#         if questionnaire_users_interest is None:
#             return jsonify({'error': 'Questionnaire Users Interest not found'}), 404
#         return jsonify(questionnaire_users_interest.serialize()), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @qn_users_interests_blueprint.route('/<int:qn_users_interest_id>', methods=['PUT'])
# def update_questionnaire_users_interest(qn_users_interest_id):
#     try:
#         data = request.get_json()
#         questionnaire_users_interest = QuestionnaireUsersInterestService.update_questionnaire_users_interest(qn_users_interest_id, data)
#         if questionnaire_users_interest is None:
#             return jsonify({'error': 'Questionnaire Users Interest not found'}), 404
#         return jsonify(questionnaire_users_interest.serialize()), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @qn_users_interests_blueprint.route('/<int:qn_users_interest_id>', methods=['DELETE'])
# def delete_questionnaire_users_interest(qn_users_interest_id):
#     try:
#         success = QuestionnaireUsersInterestService.delete_questionnaire_users_interest(qn_users_interest_id)
#         if not success:
#             return jsonify({'error': 'Questionnaire Users Interest not found'}), 404
#         return jsonify({'result': 'Questionnaire Users Interest deleted'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
