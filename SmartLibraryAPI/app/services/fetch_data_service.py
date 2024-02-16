# services/fetch_data_service.py
import requests

class FetchService:
    def __init__(self):
        # 網址有更新記得換
        self.url = "https://a72b-61-220-37-156.ngrok-free.app"

    def fetch_json_data(self):
            try:
                response = requests.get(self.url)
                response.raise_for_status()  # 確保沒有發生錯誤
                json_data = response.json()  # 解析JSON回應
                return json_data
            except requests.exceptions.RequestException as e:
                print("Error fetching JSON data:", e)
                return None
    
    def get_all_books(self):
            try:
                response = requests.get(self.url + "/api/books/")
                response.raise_for_status()  # 確保沒有發生錯誤
                json_data = response.json()  # 解析JSON回應
                return json_data
            except requests.exceptions.RequestException as e:
                print("Error fetching JSON data:", e)
                return None
            
    def get_book_by_id(self, book_id:int):
            try:
                response = requests.get(self.url + "/api/books/" + str(book_id))
                response.raise_for_status()  # 確保沒有發生錯誤
                json_data = response.json()  # 解析JSON回應
                return json_data
            except requests.exceptions.RequestException as e:
                print("Error fetching JSON data:", e)
                return None
            
    def get_all_users(self):
            try:
                response = requests.get(self.url + "/api/users/")
                response.raise_for_status()  # 確保沒有發生錯誤
                json_data = response.json()  # 解析JSON回應
                return json_data
            except requests.exceptions.RequestException as e:
                print("Error fetching JSON data:", e)
                return None
            
    def get_user_by_id(self, user_id:int):
            try:
                response = requests.get(self.url + "/api/users/" + str(user_id))
                response.raise_for_status()  # 確保沒有發生錯誤
                json_data = response.json()  # 解析JSON回應
                return json_data
            except requests.exceptions.RequestException as e:
                print("Error fetching JSON data:", e)
                return None
    # 後續根據需求自行增加
