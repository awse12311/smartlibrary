# models/books.py
from ..extensions import db

class Book(db.Model):

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.BigInteger)
    best_book_id = db.Column(db.BigInteger)
    work_id = db.Column(db.BigInteger)
    books_count = db.Column(db.Integer)
    isbn = db.Column(db.String(13))
    isbn13 = db.Column(db.BigInteger)
    title = db.Column(db.String(500), nullable=False)
    label = db.Column(db.BigInteger, db.ForeignKey('questionnaire_books_interest.id'))
    language_code = db.Column(db.String(20))
    average_rating = db.Column(db.Float)
    ratings_count = db.Column(db.BigInteger)
    work_ratings_count = db.Column(db.BigInteger)
    work_text_reviews_count = db.Column(db.BigInteger)
    image_url = db.Column(db.String(500))
    small_image_url = db.Column(db.String(500))
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.current_timestamp(), server_onupdate=db.func.current_timestamp())
    
    def serialize(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'best_book_id': self.best_book_id,
            'work_id': self.work_id,
            'books_count': self.books_count,
            'isbn': self.isbn,
            'isbn13': self.isbn13,
            'title': self.title,
            'label': self.label,
            'language_code': self.language_code,
            'average_rating': self.average_rating,
            'ratings_count': self.ratings_count,
            'work_ratings_count': self.work_ratings_count,
            'work_text_reviews_count': self.work_text_reviews_count,
            'image_url': self.image_url,
            'small_image_url': self.small_image_url,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }