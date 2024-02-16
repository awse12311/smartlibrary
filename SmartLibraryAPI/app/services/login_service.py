# services/login_service.py
from fetch_data_service import FetchService

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
                        return False, "wrong password" # 登入失敗 回傳密碼錯誤
            return False, "not found" # 登入失敗 回傳找不到該使用者
        except Exception as e:
            raise e
        
    @staticmethod
    def user_register(password, user_name:str, email:str):
        try:
            pass # 需要用post把上面三個變數傳入，然後回傳True或ID
        except Exception as e:
            raise e
