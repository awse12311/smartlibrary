from flask import request
from flask_restx import Namespace, Resource, fields
from flask import jsonify
from ..services.authors_service import AuthorService

# 建立 Namespace
authors_namespace = Namespace('authors', description='Authors related operations')

# 資料模型
author_model = authors_namespace.model('Author', {
    'id': fields.Integer(readonly=True, description='Author ID'),
    'book_id': fields.Integer(description='Book ID'),
    'author_name': fields.String(required=True, description='Author name'),
    'created_at': fields.String(description='Created at timestamp'),
    'updated_at': fields.String(description='Updated at timestamp'),
    # 如果有其他字段，可以继续添加
})

@authors_namespace.route('/')
class AuthorsResource(Resource):
    @authors_namespace.expect(author_model)
    def post(self):
        """Create a new author"""
        try:
            data = request.get_json()
            author = AuthorService.create_author(data)
            return (author.serialize()), 201
        except Exception as e:
            return ({'error': str(e)}), 500

    def get(self):
        """Get all authors"""
        try:
            authors = AuthorService.get_all_authors()
            return ([author.serialize() for author in authors]), 200
        except Exception as e:
            return ({'error': str(e)}), 500

@authors_namespace.route('/<int:author_id>')
class AuthorResource(Resource):
    def get(self, author_id):
        """Get author by ID"""
        try:
            author = AuthorService.get_author_by_id(author_id)
            if author is None:
                return ({'error': 'Author not found'}), 404
            return (author.serialize()), 200
        except Exception as e:
            return ({'error': str(e)}), 500

    @authors_namespace.expect(author_model)
    def put(self, author_id):
        """Update an author"""
        try:
            data = request.get_json()
            author = AuthorService.update_author(author_id, data)
            if author is None:
                return ({'error': 'Author not found'}), 404
            return (author.serialize()), 200
        except Exception as e:
            return ({'error': str(e)}), 500

    def delete(self, author_id):
        """Delete an author"""
        try:
            success = AuthorService.delete_author(author_id)
            if not success:
                return ({'error': 'Author not found'}), 404
            return ({'result': 'Author deleted'}), 200
        except Exception as e:
            return ({'error': str(e)}), 500

@authors_namespace.route('/batch')
class BatchAuthorsResource(Resource):
    @authors_namespace.expect([author_model])
    def post(self):
        """Create batch authors"""
        try:
            batch_data = request.json
            new_authors = AuthorService.create_batch_authors(batch_data)
            return ([author.serialize() for author in new_authors]), 201
        except Exception as e:
            return ({'error': str(e)}), 500




# # controllers/authors_controller.py
# from flask import Blueprint, request, jsonify
# from ..services.authors_service import AuthorService

# authors_blueprint = Blueprint('authors', __name__, url_prefix='/api/authors')

# @authors_blueprint.route('/', methods=['POST'])
# def create_author():
#     try:
#         data = request.get_json()
#         author = AuthorService.create_author(data)
#         return jsonify(author.serialize()), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @authors_blueprint.route('/', methods=['GET'])
# def get_authors():
#     try:
#         authors = AuthorService.get_all_authors()
#         return jsonify([author.serialize() for author in authors]), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @authors_blueprint.route('/<int:author_id>', methods=['GET'])
# def get_author(author_id):
#     try:
#         author = AuthorService.get_author_by_id(author_id)
#         if author is None:
#             return jsonify({'error': 'Author not found'}), 404
#         return jsonify(author.serialize()), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @authors_blueprint.route('/<int:author_id>', methods=['PUT'])
# def update_author(author_id):
#     try:
#         data = request.get_json()
#         author = AuthorService.update_author(author_id, data)
#         if author is None:
#             return jsonify({'error': 'Author not found'}), 404
#         return jsonify(author.serialize()), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @authors_blueprint.route('/<int:author_id>', methods=['DELETE'])
# def delete_author(author_id):
#     try:
#         success = AuthorService.delete_author(author_id)
#         if not success:
#             return jsonify({'error': 'Author not found'}), 404
#         return jsonify({'result': 'Author deleted'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # 批次處理
# @authors_blueprint.route('/batch', methods=['POST'])
# def create_batch_authors():
#     try:
#         batch_data = request.json
#         new_authors = AuthorService.create_batch_authors(batch_data)
#         return jsonify([author.serialize() for author in new_authors]), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
