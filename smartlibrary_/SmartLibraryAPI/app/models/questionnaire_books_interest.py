# models/questionnaire_books_interest.py
from ..extensions import db

Column = db.Column
Integer = db.Integer
String = db.String
TIMESTAMP = db.TIMESTAMP
func = db.func

class questionnaire_book_interest(db.Model):
    __tablename__ = 'questionnaire_books_interest'

    id = Column(Integer, primary_key=True)
    parent_interest_id = Column(Integer, db.ForeignKey('questionnaire_books_interest.id'))
    interest_name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    def serialize(self):
        return {
            'id': self.id,
            'parent_interest_id': self.parent_interest_id,
            'interest_name': self.interest_name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }