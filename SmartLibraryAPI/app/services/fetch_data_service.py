# services/fetch_data_service.py
import requests

class FetchService:
    def __init__(self):
        # 網址有更新記得換
        self.url = "https://ab90-2001-b400-e28f-b820-c581-a983-708d-19c0.ngrok-free.app"

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
            
    # 後續根據需求自行增加