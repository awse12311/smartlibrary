# services/books_service.py
from ..models.books import Book, db

class BookService:
    @staticmethod
    def create_book(data):
        try:
            book = Book(**data)
            db.session.add(book)
            db.session.commit()
            return book
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_books():
        try:
            return Book.query.all()
        except Exception as e:
            raise e

    @staticmethod
    def get_book_by_id(book_id):
        try:
            return Book.query.get(book_id)
        except Exception as e:
            raise e

    @staticmethod
    def update_book(book_id, data):
        try:
            book = BookService.get_book_by_id(book_id)
            if book is None:
                return None
            for key, value in data.items():
                setattr(book, key, value)
            db.session.commit()
            return book
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_book(book_id):
        try:
            book = BookService.get_book_by_id(book_id)
            if book is None:
                return False
            db.session.delete(book)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    # 批次處理
    @staticmethod
    def create_batch_books(batch_data):
        try:
            new_books = [Book(**data) for data in batch_data]
            db.session.add_all(new_books)
            db.session.commit()
            return new_books
        except Exception as e:
            db.session.rollback()
            raise e
