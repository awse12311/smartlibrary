# services/authors_service.py
from ..models.authors import Author, db

class AuthorService:
    @staticmethod
    def create_author(data):
        try:
            author = Author(**data)
            db.session.add(author)
            db.session.commit()
            return author
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_authors():
        try:
            return Author.query.all()
        except Exception as e:
            raise e

    @staticmethod
    def get_author_by_id(author_id):
        try:
            return Author.query.get(author_id)
        except Exception as e:
            raise e

    @staticmethod
    def update_author(author_id, data):
        try:
            author = AuthorService.get_author_by_id(author_id)
            if author is None:
                return None
            for key, value in data.items():
                setattr(author, key, value)
            db.session.commit()
            return author
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_author(author_id):
        try:
            author = AuthorService.get_author_by_id(author_id)
            if author is None:
                return False
            db.session.delete(author)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    # 批次處理
    @staticmethod
    def create_batch_authors(batch_data):
        try:
            new_authors = [Author(**data) for data in batch_data]
            db.session.add_all(new_authors)
            db.session.commit()
            return new_authors
        except Exception as e:
            db.session.rollback()
            raise e
