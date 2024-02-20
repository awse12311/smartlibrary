from flask import Flask, request, jsonify
import requests
import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 請將以下兩行更換為您的 LINE Channel 的 Access Token 和 Channel Secret
access_token = 't5aeGlq0ECw8Kc0D66THVk0KDwsX6hu21GGWaAwRo635OjRbtfzJ1/sdiWcUrr2g6sMNuRCW6VtCsYiS2MUgYLv5lJ2hCExREwBt3IgnhVbPaFgoi87y/GdiHfZhf+trP+h1kyTQ0HQHoURFwGYhTwdB04t89/1O/w1cDnyilFU='
secret = '41e777e00598a08a03e037820e0e0803'

# 請將此處替換為您的 API 圖片上傳端點和用戶註冊資料端點
# upload_image_url = 'https://yourapi.com/upload_image'
# user_book_url = 'https://yourapi.com/api/books/'
# user_data_url = 'https://yourapi.com/api/users/'
# sign_up_user = 'https://yourapi.com/api/users/'
user_book_url = 'https://a72b-61-220-37-156.ngrok-free.app/api/books/'
user_data_url = 'https://a72b-61-220-37-156.ngrok-free.app/api/users/'
sign_up_user = 'https://a72b-61-220-37-156.ngrok-free.app/api/users/'

line_bot_api = LineBotApi(access_token)  # 初始化 LineBotApi 實例
handler = WebhookHandler(secret)  # 初始化 WebhookHandler 實例

# 登錄狀態的全域變數
logged_in = False
current_account = None
waiting_for_account = None
registration_state = 0
registration_email = None
registration_username = None
registration_password = None

# 定義 Flask 路由處理啟動時的介紹訊息
@app.route("/", methods=['GET'])
def introduction():
    # 發送介紹訊息
    intro_message = "歡迎使用我們的聊天機器人！這是一個圖書館介紹機器人，您可以詢問有關圖書館的任何問題。"
    return jsonify({"message": intro_message})

@app.route("/", methods=['POST'])
def linebot():
    global logged_in
    global current_account
    global registration_state
    global registration_email
    global registration_username
    global registration_password

    signature = request.headers['X-Line-Signature']  # 從請求標頭中獲取簽名
    body = request.get_data(as_text=True)  # 從請求中獲取消息內容
    json_data = json.loads(body)  # 將消息內容解析為 JSON 格式
    
    try:
        handler.handle(body, signature)  # 驗證簽名，處理 Webhook 事件
        events = json_data['events']  # 獲取事件列表
        
        for event in events:
            tk = event['replyToken']  # 取得回傳訊息的 Token
            type = event['message']['type']  # 取得 LINE 收到的訊息類型
            
            # 判斷如果是文字
            if type == 'text':
                handle_text_message(event, tk)
            else:
                reply = '你傳的不是文字呦～'
                line_bot_api.reply_message(tk, TextSendMessage(reply))  # 回傳訊息
    except:
        print(body)  # 如果發生錯誤，印出收到的內容
    
    return 'OK' 

def handle_text_message(event, tk):
    global logged_in
    global current_account
    global waiting_for_account
    global registration_state
    global registration_email
    global registration_username
    global registration_password

    msg = event['message']['text']  # 獲取文字消息內容
    
    # 處理用戶發送的訊息
    if '註冊' in msg:
        if logged_in:
            # 如果已經登入，提示無需註冊
            reply_text = "您已經登入，無須註冊。"
            line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
        else:
            # 處理註冊流程
            registration_state = 1  # 設置註冊狀態為 1
            registration_email = None  # 清除先前的註冊資訊
            registration_username = None
            registration_password = None
            reply_text = '請輸入您的電子郵件地址：'  # 提示用戶輸入電子郵件地址
            line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))

    # 處理用戶註冊流程
    # 處理用戶註冊流程
    elif registration_state == 1: # 如果用戶註冊的狀態為 1
        try:
            response = requests.get(user_data_url)
            if response.status_code == 200:
                user_data = response.json()
                email = msg.strip()  # 獲取用戶輸入的電子郵件地址

                if check_email(user_data, email):  # 如果電子郵件地址已存在
                    reply_text = '該電子郵件地址已被使用，請重新輸入：'  # 提示用戶重新輸入
                else:
                    reply_text = '請輸入您的使用者名稱：'  # 提示用戶輸入使用者名稱
                    line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
                    registration_state += 1  # 將用戶狀態加 1，以便下一步驟
                    # 更新註冊資訊
                    registration_email = email
            else:
                reply_text = '無法連接到用戶資料伺服器，請檢查網路連接並稍後再試。'
        except requests.exceptions.RequestException as e:
            reply_text = '與伺服器通訊時發生錯誤，請稍後再試。'
        line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))


    # 處理用戶註冊流程
    elif registration_state == 2:  # 如果用戶註冊的狀態為 2
        try:
            response = requests.get(user_data_url)
            if response.status_code == 200:
                user_data = response.json()
                username = msg.strip()  # 獲取用戶輸入的使用者名稱

                if check_username(user_data, username):  # 如果使用者名稱已存在
                    reply_text = '該使用者名稱已被使用，請重新輸入：'  # 提示用戶重新輸入
                else:
                    reply_text = '請輸入您的密碼：'  # 提示用戶輸入密碼
                    line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
                    registration_state += 1  # 將用戶狀態加 1，以便下一步驟
                    # 更新註冊資訊
                    registration_username = username
            else:
                reply_text = '無法連接到用戶資料伺服器，請檢查網路連接並稍後再試。'
        except requests.exceptions.RequestException as e:
            reply_text = '與伺服器通訊時發生錯誤，請稍後再試。'
        line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))

    
    # 處理用戶註冊流程
    elif registration_state == 3:  # 如果用戶的狀態為 3
        password = msg  # 獲取用戶輸入的密碼
        # 更新註冊資訊
        registration_password = password
        registration_state = 0 #歸零用戶註冊的狀態

        if register_user(registration_username, registration_password, registration_email):
            reply_text = '註冊成功！'
        else:
            reply_text = '註冊失敗。請稍後再試。'
        line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))  

    elif '登入' in msg or '登陸' in msg or '登錄' in msg:
        if logged_in:
            reply_text = "已經登入完成了"
        else:
            # 提示用戶先輸入帳號
            reply_text = "請登入使用者帳號"
            # 將消息設置為等待輸入帳號狀態
            waiting_for_account = True
            current_account = None
        line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
    elif waiting_for_account == True:
        # 如果正在等待用戶輸入帳號
        account = msg.strip()  # 移除前後空格

        try:
            response = requests.get(user_data_url)
            if response.status_code == 200:
                user_data = response.json()
                if check_account(user_data, account):
                    # 設置當前帳號
                    current_account = account
                    # 請求輸入密碼
                    reply_text = '請輸入密碼'
                    line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
                    # 不再等待輸入帳號
                    waiting_for_account = False
                else:
                    # 帳號不存在，提示重新輸入帳號
                    reply_text = '帳號不存在，請重新輸入帳號。'
                    line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
            else:
                reply_text = '無法連接到用戶資料伺服器，請檢查網路連接並稍後再試。'
                line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
                logged_in = False
        except requests.exceptions.RequestException as e:
            reply_text = '與伺服器通訊時發生錯誤，請稍後再試。'
            line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
            logged_in = False

    elif current_account is not None and not logged_in:
        # 已經輸入了帳號，但尚未登入，現在輸入密碼
        password = msg
        response = requests.get(user_data_url)
        if response.status_code == 200:
            user_data = response.json()
            # 驗證密碼是否正確
            if check_password(user_data, current_account, password):
                # 登入成功
                logged_in = True
                line_bot_api.reply_message(tk, TextSendMessage(text="登入成功！現在您可以使用進階功能了。"))
            else:
                # 密碼錯誤，要求重新輸入密碼
                reply_text = '密碼錯誤，請重新輸入密碼。'
                line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
        else:
            reply_text = '無法獲取用戶資料。'
            line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))

    else:
        # 進階功能(在此處新增判斷功能指令)
        if logged_in:
            if msg.startswith('/search'):
                search_books(event, tk)
            elif msg.startswith('/details'):
                show_book_details(event, tk)
            else:
                # 如果收到未知指令，回覆提示
                reply_text = "請輸入有效的指令，如：\n/search keyword - 搜尋書籍\n/details book_name - 顯示書籍詳細資訊"
                line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
        else:
            # 如果未登錄，直接回覆用戶輸入的訊息
            reply_text = msg
            line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))

# 定義函式用於新增用戶資料到 API
def register_user(username, password, email):
    data = {
        "username": username,
        "password": password,
        "email": email
        #"face_recognition_image_path": None
    }

    try:
        response = requests.post(sign_up_user, json=data)  # 向 API 發送 POST 請求提交用戶資料
        if response.status_code == 201:
            return True  # 如果註冊成功，返回 True
        else:
            return False  # 如果註冊失敗，返回 False
    except requests.exceptions.RequestException as e:
        print(e)  # 請求異常，印出錯誤訊息
        return False  # 返回 False，表示註冊失敗


# 用於檢查帳號是否存在的函式
def check_account(user_data, account):
    for data in user_data:
        if account == str(data['username']):
            return True

# 用於檢查密碼是否正確的函式
def check_password(user_data, account, password):
    for data in user_data:
        if account == str(data['username']) and password == str(data['password']):
            return True

# 用於檢查電子郵件地址是否已存在的函式
def check_email(user_data, email):
    for data in user_data:
        if email == str(data['email']):
            return True
    return False

# 用於檢查使用者名稱是否已存在的函式
def check_username(user_data, username):
    for data in user_data:
        if username == str(data['username']):
            return True
    return False

def search_books(event, tk):
    global logged_in
    if not logged_in:
        reply_text = "請先登錄，請輸入 /login 帳號 密碼 進行登錄。"
        line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
        return

    msg = event['message']['text']
    keyword = msg.split(' ', 1)[1].lower()

    response = requests.get(user_book_url)
    if response.status_code == 200:
        user_book_data = response.json()

        search_results = [book for book in user_book_data if keyword in book['title'].lower()]
        if search_results:
            reply_text = "以下是符合搜尋條件的書籍：\n"
            for i, book in enumerate(search_results, 1):
                reply_text += f"{i}. {book['title']} - 書籍ID：{book['book_id']}\n"
        else:
            reply_text = "找不到符合搜尋條件的書籍。"
    else:
        reply_text = '無法獲取書籍資料。'

    line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))

def show_book_details(event, tk):
    global logged_in
    if not logged_in:
        reply_text = "請先登錄，請輸入 /login 帳號 密碼 進行登錄。"
        line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
        return

    msg = event['message']['text']
    book_name = msg.split(' ', 1)[1].lower()  # 將用戶輸入的書名轉換為小寫字母

    response = requests.get(user_book_url)
    if response.status_code == 200:
        user_book_data = response.json()

        # 直接比較用戶輸入的書名與書籍列表中的書名
        for book in user_book_data:
            if book_name == book['title'].lower():
                # 找到匹配的書籍，構建詳細資訊的回覆訊息
                reply_text = f"書籍詳細資訊：\n"
                for key, value in book.items():
                    reply_text += f"{key}: {value}\n"
                line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
                return
        # 如果沒有找到匹配的書籍
        reply_text = "找不到指定名稱的書籍。"
    else:
        reply_text = '無法獲取書籍資料。'

    line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    app.run(debug=True)  # 在 debug 模式下運行 Flask 應用程式


