# services/recommend_service.py
from .fetch_data_service import FetchService

class RecommendService:
    def __init__(self):
        self.book_data = FetchService().get_all_books()

    def recommend_books_for_user(self, user_ins): #用list列出使用者的所有興趣項目
        # 根據使用者的喜好將書本過濾並依評分排序
        recommend_books = []
        for ins in user_ins:
            book_list = [[book['title'], book['label'], book['average_rating']] for book in self.book_data if book['label'] == int(ins)]
            recommend_books.append(sorted(book_list, key=lambda x: x[2], reverse=True))
        recommend_number = 15

        # 計算應該拿書本的輪次和額外挑選的
        choose_number = recommend_number // len(user_ins)
        extra_choose = recommend_number % len(user_ins)
        # 根據輪次拿取書本
        result = []
        for number in range(choose_number):
            for interest_book_list in recommend_books:
                result.append(interest_book_list.pop(0))

        # 把最後一列拿出來並處理額外挑選
        extra_list = []
        for extra in recommend_books:
            extra_list.append(extra[0])
        sort_list = sorted(extra_list, key=lambda x: x[2], reverse=True)
        result.extend(sort_list[:extra_choose])

        return result
        
if __name__ == "__main__":
    recom = RecommendService().recommend_books_for_user(user_ins=[5, 7, 8, 9])
    print(recom)