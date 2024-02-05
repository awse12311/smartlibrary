# services/ratings_service.py
from ..models.ratings import Rating, db

class RatingService:
    @staticmethod
    def create_rating(data):
        try:
            rating = Rating(**data)
            db.session.add(rating)
            db.session.commit()
            return rating
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_ratings():
        try:
            return Rating.query.all()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_rating_by_id(rating_id):
        try:
            return Rating.query.get(rating_id)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_rating(rating_id, data):
        try:
            rating = RatingService.get_rating_by_id(rating_id)
            if rating is None:
                return None
            for key, value in data.items():
                setattr(rating, key, value)
            db.session.commit()
            return rating
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_rating(rating_id):
        try:
            rating = RatingService.get_rating_by_id(rating_id)
            if rating is None:
                return False
            db.session.delete(rating)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    # 批次處理
    @staticmethod
    def create_batch_ratings(batch_data):
        try:
            new_ratings = [Rating(**data) for data in batch_data]
            db.session.add_all(new_ratings)
            db.session.commit()
            return new_ratings
        except Exception as e:
            db.session.rollback()
            raise e
