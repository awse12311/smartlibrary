# services/recommend_service.py
from .fetch_data_service import FetchService

class RecommendService:
    def __init__(self):
        self.book_data = FetchService().get_all_books()

    def recommend_books_for_user(self, user_ins): #用list列出使用者的所有興趣項目
        recommend_books = [[book['title'], book['label'], book['average_rating']] for book in self.book_data if book in user_ins]

        count = 10 / user_ins
        recommend_list = []
        for label in user_ins:
            while len(recommend_list) < 10

        pass 
        