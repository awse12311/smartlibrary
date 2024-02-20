# services/login_service.py
from .fetch_data_service import FetchService

class LoginService:

    @staticmethod
    def user_login_check(email:str, password:str): # 可透過電子信箱登入
        try:
            user_infomation = FetchService().get_all_users()
            for user in user_infomation:
                if email == user["email"]:
                    if password == user["password"]:
                        return True, user["username"] # 登入成功 回傳使用者名稱
                    else:
                        return False, "密碼錯誤" # 登入失敗 回傳密碼錯誤
            return False, "找不到該使用者" # 登入失敗 回傳找不到該使用者
        except Exception as e:
            raise e
        
    @staticmethod
    def user_register(username:str, email:str, password):
        try:
            data = {
            "username": username,
            "password": password,
            "email": email
            }
            result = FetchService().user_register(data=data)
            return result
        except Exception as e:
            raise e
