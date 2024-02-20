# controllers/questionnaire_book_interest_service.py
from psycopg2 import IntegrityError
from ..models.questionnaire_books_interest import questionnaire_book_interest, db

class questionnaire_book_interest_service:
    
    @staticmethod
    def create_interest(data):
        try:
            interest = questionnaire_book_interest(**data)
            db.session.add(interest)
            db.session.commit()
            return interest
        except IntegrityError:
            db.session.rollback()
            raise IntegrityError('Duplicate key value violates unique constraint')

    @staticmethod
    def get_all_interests():
        try:
            return questionnaire_book_interest.query.all()
        except Exception as e:
            raise e

    @staticmethod
    def get_interest_by_id(interest_id):
        try:
            return questionnaire_book_interest.query.get(interest_id)
        except Exception as e:
            raise e

    @staticmethod
    def update_interest(interest_id, data):
        try:
            interest = questionnaire_book_interest_service.get_interest_by_id(interest_id)
            if interest is None:
                return None
            for key, value in data.items():
                setattr(interest, key, value)
            db.session.commit()
            return interest
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_interest(interest_id):
        try:
            interest = questionnaire_book_interest_service.get_interest_by_id(interest_id)
            if interest is None:
                return False, 'Interest not found'
            db.session.delete(interest)
            db.session.commit()
            return True, 'Interest deleted'
        except Exception as e:
            db.session.rollback()
            raise e

    # 批次處理
    @staticmethod
    def create_batch_interests(batch_data):
        try:
            new_interests = [questionnaire_book_interest(**data) for data in batch_data]
            db.session.add_all(new_interests)
            db.session.commit()
            return new_interests
        except IntegrityError:
            db.session.rollback()
            raise IntegrityError('Duplicate key value violates unique constraint')
