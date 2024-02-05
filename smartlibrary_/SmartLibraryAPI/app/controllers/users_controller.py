# controllers/users_controller.py
from flask import request
from flask_restx import Namespace, Resource, fields
from flask import jsonify
from ..services.users_service import UserService

# 建立 Namespace
users_namespace = Namespace('users', description='Users related operations')

# 資料模型
user_model = users_namespace.model('User', {
    'user_id': fields.Integer(description='User ID'),
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
    'email': fields.String(required=True, description='Email'),
    'face_recognition_image_path': fields.String(description='Face recognition image path'),
    'created_at': fields.String(description='Created at timestamp'),
    'updated_at': fields.String(description='Updated at timestamp'),
})

@users_namespace.route('/')
class UserResource(Resource):
    @users_namespace.expect(user_model)
    def post(self):
        """Create a new user"""
        try:
            data = request.get_json()
            user = UserService.create_user(data)
            return (user.serialize()), 201
        except Exception as e:
            return ({'error': str(e)}), 500

    def get(self):
        """Get all users"""
        try:
            users = UserService.get_all_users()
            return ([user.serialize() for user in users]), 200
        except Exception as e:
            return ({'error': str(e)}), 500

@users_namespace.route('/<int:user_id>')
class UserDetailResource(Resource):
    def get(self, user_id):
        """Get user by ID"""
        try:
            user = UserService.get_user_by_id(user_id)
            if user is None:
                return ({'error': 'User not found'}), 404
            return (user.serialize()), 200
        except Exception as e:
            return ({'error': str(e)}), 500

    @users_namespace.expect(user_model)
    def put(self, user_id):
        """Update a user"""
        try:
            data = request.get_json()
            user = UserService.update_user(user_id, data)
            if user is None:
                return ({'error': 'User not found'}), 404
            return (user.serialize()), 200
        except Exception as e:
            return ({'error': str(e)}), 500

    def delete(self, user_id):
        """Delete a user"""
        try:
            success = UserService.delete_user(user_id)
            if not success:
                return ({'error': 'User not found'}), 404
            return ({'result': 'User deleted'}), 200
        except Exception as e:
            return ({'error': str(e)}), 500

@users_namespace.route('/batch')
class BatchUserResource(Resource):
    @users_namespace.expect([user_model])
    def post(self):
        """Create batch users"""
        try:
            batch_data = request.json
            new_users = UserService.create_batch_users(batch_data)
            return ([user.serialize() for user in new_users]), 201
        except Exception as e:
            return ({'error': str(e)}), 500




# from flask import Blueprint, request, jsonify
# from ..services.users_service import UserService

# users_blueprint = Blueprint('users', __name__, url_prefix='/api/users')

# @users_blueprint.route('/', methods=['POST'])
# def create_user():
#     try:
#         data = request.get_json()
#         user = UserService.create_user(data)
#         return jsonify(user.serialize()), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @users_blueprint.route('/', methods=['GET'])
# def get_users():
#     try:
#         users = UserService.get_all_users()
#         return jsonify([user.serialize() for user in users]), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @users_blueprint.route('/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     try:
#         user = UserService.get_user_by_id(user_id)
#         if user is None:
#             return jsonify({'error': 'User not found'}), 404
#         return jsonify(user.serialize()), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @users_blueprint.route('/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     try:
#         data = request.get_json()
#         user = UserService.update_user(user_id, data)
#         if user is None:
#             return jsonify({'error': 'User not found'}), 404
#         return jsonify(user.serialize()), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @users_blueprint.route('/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     try:
#         success = UserService.delete_user(user_id)
#         if not success:
#             return jsonify({'error': 'User not found'}), 404
#         return jsonify({'result': 'User deleted'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # 批次處理
# @users_blueprint.route('/batch', methods=['POST'])
# def create_batch_users():
#     try:
#         batch_data = request.json
#         new_users = UserService.create_batch_users(batch_data)
#         return jsonify([user.serialize() for user in new_users]), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
