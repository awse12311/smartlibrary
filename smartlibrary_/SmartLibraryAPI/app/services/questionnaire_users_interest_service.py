# services/questionnaire_users_interest_service.py

from ..models.questionnaire_users_interest import QuestionnaireUsersInterest, db

class QuestionnaireUsersInterestService:
    @staticmethod
    def create_questionnaire_users_interest(data):
        try:
            questionnaire_users_interest = QuestionnaireUsersInterest(**data)
            db.session.add(questionnaire_users_interest)
            db.session.commit()
            return questionnaire_users_interest
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_questionnaire_users_interests():
        try:
            return QuestionnaireUsersInterest.query.all()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_questionnaire_users_interest_by_id(qn_users_interest_id):
        try:
            return QuestionnaireUsersInterest.query.get(qn_users_interest_id)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_questionnaire_users_interest(qn_users_interest_id, data):
        try:
            questionnaire_users_interest = QuestionnaireUsersInterestService.get_questionnaire_users_interest_by_id(qn_users_interest_id)
            if questionnaire_users_interest is None:
                return None
            for key, value in data.items():
                setattr(questionnaire_users_interest, key, value)
            db.session.commit()
            return questionnaire_users_interest
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_questionnaire_users_interest(qn_users_interest_id):
        try:
            questionnaire_users_interest = QuestionnaireUsersInterestService.get_questionnaire_users_interest_by_id(qn_users_interest_id)
            if questionnaire_users_interest is None:
                return False
            db.session.delete(questionnaire_users_interest)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    # 批次處理
    @staticmethod
    def create_batch_questionnaire_users_interests(batch_data):
        try:
            new_questionnaire_users_interests = [QuestionnaireUsersInterest(**data) for data in batch_data]
            db.session.add_all(new_questionnaire_users_interests)
            db.session.commit()
            return new_questionnaire_users_interests
        except Exception as e:
            db.session.rollback()
            raise e
