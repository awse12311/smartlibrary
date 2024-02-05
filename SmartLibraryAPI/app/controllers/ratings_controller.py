# controllers/ratings_controller.py

from flask import request
from flask_restx import Namespace, Resource, fields
from flask import jsonify
from ..services.ratings_service import RatingService

# 建立 Namespace
ratings_namespace = Namespace('ratings', description='Ratings related operations')

# 資料模型
rating_model = ratings_namespace.model('Rating', {
    'id': fields.Integer(readonly=True,description='Rating ID'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'book_id': fields.Integer(required=True, description='Book ID'),
    'rating': fields.Integer(description='Rating'),
    'created_at': fields.String(description='Created at timestamp'),
    'updated_at': fields.String(description='Updated at timestamp'),
})

@ratings_namespace.route('/')
class RatingResource(Resource):
    @ratings_namespace.expect(rating_model)
    def post(self):
        """Create a new rating"""
        try:
            data = request.get_json()
            rating = RatingService.create_rating(data)
            return (rating.serialize()), 201
        except Exception as e:
            return ({'error': str(e)}), 500

    def get(self):
        """Get all ratings"""
        try:
            ratings = RatingService.get_all_ratings()
            return ([rating.serialize() for rating in ratings]), 200
        except Exception as e:
            return ({'error': str(e)}), 500

@ratings_namespace.route('/<int:rating_id>')
class RatingDetailResource(Resource):
    def get(self, rating_id):
        """Get rating by ID"""
        try:
            rating = RatingService.get_rating_by_id(rating_id)
            if rating is None:
                return ({'error': 'Rating not found'}), 404
            return (rating.serialize()), 200
        except Exception as e:
            return ({'error': str(e)}), 500

    @ratings_namespace.expect(rating_model)
    def put(self, rating_id):
        """Update a rating"""
        try:
            data = request.get_json()
            rating = RatingService.update_rating(rating_id, data)
            if rating is None:
                return ({'error': 'Rating not found'}), 404
            return (rating.serialize()), 200
        except Exception as e:
            return ({'error': str(e)}), 500

    def delete(self, rating_id):
        """Delete a rating"""
        try:
            success = RatingService.delete_rating(rating_id)
            if not success:
                return ({'error': 'Rating not found'}), 404
            return ({'result': 'Rating deleted'}), 200
        except Exception as e:
            return ({'error': str(e)}), 500

@ratings_namespace.route('/batch')
class BatchRatingResource(Resource):
    @ratings_namespace.expect([rating_model])
    def post(self):
        """Create batch ratings"""
        try:
            batch_data = request.json
            new_ratings = RatingService.create_batch_ratings(batch_data)
            return ([rating.serialize() for rating in new_ratings]), 201
        except Exception as e:
            return ({'error': str(e)}), 500


# from flask import Blueprint, request, jsonify
# from ..services.ratings_service import RatingService

# ratings_blueprint = Blueprint('ratings', __name__, url_prefix='/api/ratings')

# @ratings_blueprint.route('/', methods=['POST'])
# def create_rating():
#     try:
#         data = request.get_json()
#         rating = RatingService.create_rating(data)
#         return jsonify(rating.serialize()), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @ratings_blueprint.route('/', methods=['GET'])
# def get_ratings():
#     try:
#         ratings = RatingService.get_all_ratings()
#         return jsonify([rating.serialize() for rating in ratings]), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @ratings_blueprint.route('/<int:rating_id>', methods=['GET'])
# def get_rating(rating_id):
#     try:
#         rating = RatingService.get_rating_by_id(rating_id)
#         if rating is None:
#             return jsonify({'error': 'Rating not found'}), 404
#         return jsonify(rating.serialize()), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @ratings_blueprint.route('/<int:rating_id>', methods=['PUT'])
# def update_rating(rating_id):
#     try:
#         data = request.get_json()
#         rating = RatingService.update_rating(rating_id, data)
#         if rating is None:
#             return jsonify({'error': 'Rating not found'}), 404
#         return jsonify(rating.serialize()), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @ratings_blueprint.route('/<int:rating_id>', methods=['DELETE'])
# def delete_rating(rating_id):
#     try:
#         success = RatingService.delete_rating(rating_id)
#         if not success:
#             return jsonify({'error': 'Rating not found'}), 404
#         return jsonify({'result': 'Rating deleted'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # 批次處理
# @ratings_blueprint.route('/batch', methods=['POST'])
# def create_batch_ratings():
#     try:
#         batch_data = request.json
#         new_ratings = RatingService.create_batch_ratings(batch_data)
#         return jsonify([rating.serialize() for rating in new_ratings]), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
