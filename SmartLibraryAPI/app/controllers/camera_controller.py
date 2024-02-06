from flask import request
from flask_restx import Namespace, Resource, fields
from flask import jsonify
from ..services.camera_service import CameraService

# 建立 Namespace
camera_namespace = Namespace('camera', description='Camera related operations')

@camera_namespace.route('/')
class CameraResource(Resource):
    # 針對單一畫面進行臉部識別
    def face_recognition(self):
        """Recognize face"""
        try:
            result = CameraService.recogintion_face_for_image()
            # result: 判定結果:
            # 沒有偵測到臉: "no_face" 
            # 臉部數量超過: "over_face" 
            # 找到臉但沒有搜尋到匹配者: "no_register" 
            # 搜尋到匹配者: user_id(類型為int))
            return result , 201
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
