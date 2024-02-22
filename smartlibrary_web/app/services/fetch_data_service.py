# services/fetch_data_service.py
import requests

class FetchService:
    def __init__(self):
        # 網址有更新記得換
        self.url = "https://a102-61-220-37-156.ngrok-free.app/"

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
            
    def user_register_data(self, data):
        try:
            sign_up_user = self.url + "/api/users/"
            response = requests.post(sign_up_user, json=data)  # 向 API 發送 POST 請求提交用戶資料
            if response.status_code == 201:
                user_list = self.get_all_users()
                # 遍歷所有用戶資料 確認信箱符合後回傳ID
                user_id = [user["user_id"] for user in user_list if user["email"] == data["email"]]
                return True, user_id[0]  # 如果註冊成功，返回 使用者ID
            else:
                return False, "該信箱已被註冊"  # 如果註冊失敗，返回 False
        except requests.exceptions.RequestException as e:
            print(e)  # 請求異常，印出錯誤訊息
            return False  # 返回 False，表示註冊失敗
        
    def save_user_interests_to_data(self, user_ins, user_id):
        try:
            user_interests = self.url + "/api/questionnaire_users_interests/"
            for ins in user_ins:
                data = {
                "user_id": int(user_id),
                "interests_id": int(ins)
                }
                response = requests.post(user_interests, json=data)
                if response.status_code != 201:
                    print("ERROR")
                else:
                    print("SAVE_OK")
        except requests.exceptions.RequestException as e:
            print("Error fetching JSON data:", e)
            return None
        
    def get_all_interest(self):
        try:
            response = requests.get(self.url + "/api/questionnaire_users_interests/")
            response.raise_for_status()  # 確保沒有發生錯誤
            json_data = response.json()  # 解析JSON回應
            return json_data
        except requests.exceptions.RequestException as e:
            print("Error fetching JSON data:", e)
            return None

    def get_user_interest_by_id(self, user_id):
        interest = self.get_all_interest()
        interest_list = []
        for ins in interest:
            if ins["user_id"] == int(user_id):
                interest_list.append(ins["interests_id"])
        return list(set(interest_list))
                 
        
if __name__ == "__main__":
    #FetchService().save_user_interests_to_data(user_id=1, user_ins=[1,2,3,4])
    pass
