from flask import request
from flask_restx import Namespace, Resource, fields
from flask import jsonify
from ..services.books_service import BookService
from ..models.books import Book
# 建立 Namespace
books_namespace = Namespace('books', description='Books related operations')

# 資料模型
book_model = books_namespace.model('Book', {
    'book_id': fields.Integer(description='Book ID'),
    'best_book_id': fields.Integer(description='Best Book ID'),
    'work_id': fields.Integer(description='Work ID'),
    'books_count': fields.Integer(description='Books count'),
    'isbn': fields.String(description='ISBN'),
    'isbn13': fields.Integer(description='ISBN13'),
    'title': fields.String(required=True, description='Book title'),
    'label': fields.Integer(description='Label'),
    'language_code': fields.String(description='Language code'),
    'average_rating': fields.Float(description='Average rating'),
    'ratings_count': fields.Integer(description='Ratings count'),
    'work_ratings_count': fields.Integer(description='Work ratings count'),
    'work_text_reviews_count': fields.Integer(description='Work text reviews count'),
    'image_url': fields.String(description='Image URL'),
    'small_image_url': fields.String(description='Small image URL'),
    'created_at': fields.String(description='Created at timestamp'),
    'updated_at': fields.String(description='Updated at timestamp'),
})

@books_namespace.route('/')
class BooksResource(Resource):
    @books_namespace.expect(book_model)
    def post(self):
        """Create a new book"""
        try:
            data = request.get_json()
            book = BookService.create_book(data)
            return (book.serialize()), 201
        except Exception as e:
            return ({'error': str(e)}), 500

    def get(self):
        """Get all books"""
        try:
            books = BookService.get_all_books()
            return ([book.serialize() for book in books]), 200
        except Exception as e:
            return ({'error': str(e)}), 500

@books_namespace.route('/<int:id>')
class BookResource(Resource):
    def get(self, id):
        """Get book by ID"""
        try:
            book = BookService.get_book_by_id(id)
            if book is None:
                return ({'error': 'Book not found'}), 404
            return book.serialize(), 200
        except Exception as e:
            return ({'error': str(e)}), 500

    @books_namespace.expect(book_model)
    def put(self, id):
        """Update a book"""
        try:
            data = request.get_json()
            book = BookService.update_book(id, data)
            if book is None:
                return ({'error': 'Book not found'}), 404
            return (book.serialize()), 200
        except Exception as e:
            return ({'error': str(e)}), 500

    def delete(self, id):
        """Delete a book"""
        try:
            success = BookService.delete_book(id)
            if not success:
                return ({'error': 'Book not found'}), 404
            return ({'result': 'Book deleted'}), 200
        except Exception as e:
            return ({'error': str(e)}), 500

@books_namespace.route('/batch')
class BatchBooksResource(Resource):
    @books_namespace.expect([book_model])
    def post(self):
        """Create batch books"""
        try:
            batch_data = request.json
            new_books = BookService.create_batch_books(batch_data)
            return ([book.serialize() for book in new_books]), 201
        except Exception as e:
            return ({'error': str(e)}), 500



# # controllers/books_controller.py
# from flask import Blueprint, request, jsonify
# from ..services.books_service import BookService

# books_blueprint = Blueprint('books', __name__, url_prefix='/api/books')

# @books_blueprint.route('/', methods=['POST'])
# def create_book():
#     try:
#         data = request.get_json()
#         book = BookService.create_book(data)
#         return jsonify(book.serialize()), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @books_blueprint.route('/', methods=['GET'])
# def get_books():
#     try:
#         books = BookService.get_all_books()
#         return jsonify([book.serialize() for book in books]), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @books_blueprint.route('/<int:id>', methods=['GET'])
# def get_book(id):
#     try:
#         book = BookService.get_book_by_id(id)
#         if book is None:
#             return jsonify({'error': 'Book not found'}), 404
#         return jsonify(book.serialize()), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @books_blueprint.route('/<int:id>', methods=['PUT'])
# def update_book(id):
#     try:
#         data = request.get_json()
#         book = BookService.update_book(id, data)
#         if book is None:
#             return jsonify({'error': 'Book not found'}), 404
#         return jsonify(book.serialize()), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @books_blueprint.route('/<int:id>', methods=['DELETE'])
# def delete_book(id):
#     try:
#         success = BookService.delete_book(id)
#         if not success:
#             return jsonify({'error': 'Book not found'}), 404
#         return jsonify({'result': 'Book deleted'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # 批次處理
# @books_blueprint.route('/batch', methods=['POST'])
# def create_batch_books():
#     try:
#         batch_data = request.json
#         new_books = BookService.create_batch_books(batch_data)
#         return jsonify([book.serialize() for book in new_books]), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
