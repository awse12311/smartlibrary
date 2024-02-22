# services/login_service.py
from .fetch_data_service import FetchService
from .camera_service import CameraService

class LoginService:

    @staticmethod
    def user_login_check(email:str, password:str): # 可透過電子信箱登入
        try:
            user_infomation = FetchService().get_all_users()
            
            for user in user_infomation:
                if email == user["email"]:
                    if password == user["password"]:
                        return True, user # 登入成功 回傳使用者資料
                    else:
                        return False, "密碼錯誤" # 登入失敗 回傳密碼錯誤
            return False, "找不到該使用者" # 登入失敗 回傳找不到該使用者
        except Exception as e:
            raise e
        
    @staticmethod
    def user_register(username:str, email:str, password, booktype):
        try:
            data = {
            "username": username,
            "password": password,
            "email": email
            }
            # 使用POST進行註冊
            check, result = FetchService().user_register_data(data=data)
            if check:
                # 儲存暫存檔到資料庫並命名為ID
                CameraService().save_temp_to_data(user_id=result)
                # 儲存使用者的喜好到資料庫
                FetchService().save_user_interests_to_data(user_ins=booktype, user_id=result)
            return check, result
        except Exception as e:
            raise e

    @staticmethod
    def user_login_with_face():
        result = CameraService().recogintion_face_for_image()
        if result not in ["no_face", "over_face", "no_register"]:
            return True, result
        else:
            return False, result

if __name__ == "__main__":
    # result = LoginService.user_register(username="7441444", email="7441444", password="7441444")
    # print(result)
    pass
