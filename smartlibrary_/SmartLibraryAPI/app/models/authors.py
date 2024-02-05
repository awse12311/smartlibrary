# models/authors.py

from ..extensions import db,Column,Integer,ForeignKey,String,TIMESTAMP,func


class Author(db.Model):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    author_name = Column(String(500), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.current_timestamp(), server_onupdate=func.current_timestamp())

    def serialize(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'author_name': self.author_name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
