from ..extensions import db


class QuestionnaireUsersInterest(db.Model):
    __tablename__ = 'questionnaire_users_interest'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    interests_id = db.Column(db.Integer) 
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(), server_onupdate=db.func.current_timestamp())

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'interests_id': self.interests_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
