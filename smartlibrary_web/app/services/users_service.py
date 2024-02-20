# services/users_service.py
from ..models.users import User, db

class UserService:
    @staticmethod
    def create_user(data):
        try:
            user = User(**data)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_users():
        try:
            return User.query.all()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_user_by_id(user_id):
        try:
            return User.query.get(user_id)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_user(user_id, data):
        try:
            user = UserService.get_user_by_id(user_id)
            if user is None:
                return None
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_user(user_id):
        try:
            user = UserService.get_user_by_id(user_id)
            if user is None:
                return False
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    # 批次處理
    @staticmethod
    def create_batch_users(batch_data):
        try:
            new_users = [User(**data) for data in batch_data]
            db.session.add_all(new_users)
            db.session.commit()
            return new_users
        except Exception as e:
            db.session.rollback()
            raise e
