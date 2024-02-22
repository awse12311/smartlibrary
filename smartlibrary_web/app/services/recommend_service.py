# services/recommend_service.py
from .fetch_data_service import FetchService

class RecommendService:
    def __init__(self):
        self.book_data = FetchService().get_all_books()

    def recommend_books_for_user(self, user_ins): #用list列出使用者的所有興趣項目
        # 對照字典
        interest_dict = {
            1:"藝術文學",
            2:"傳記與回憶錄",
            3:"教育與參考資料",
            4:"健康生活",
            5:"文學",
            6:"歷史文化",
            7:"小說",
            8:"宗教哲學",
            9:"科學自然",
            10:"社會科學",
            11:"旅遊地理"
        }
        
        # 根據使用者的喜好將書本過濾並依評分排序
        recommend_books = []
        for ins in user_ins:
            book_list = [[book['title'], interest_dict[int(book['label'])], book['average_rating'], book['image_url']] for book in self.book_data if book['label'] == int(ins)]
            recommend_books.append(sorted(book_list, key=lambda x: x[2], reverse=True))
            # print("興趣 "+ str(ins))
            # print(len(book_list))
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
    recom = RecommendService().recommend_books_for_user(user_ins=[5, 3, 7])
    print(recom)