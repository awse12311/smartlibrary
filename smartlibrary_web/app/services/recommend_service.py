# services/recommend_service.py
from .fetch_data_service import FetchService

class RecommendService:
    def __init__(self):
        self.book_data = FetchService().get_all_books()

    def recommend_books_for_new_user(self, user_ins): #用list列出使用者的所有興趣項目
        pass