from flask import Flask, request, jsonify
import requests
import json
import re
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import random
app = Flask(__name__)

# 請將以下兩行更換為您的 LINE Channel 的 Access Token 和 Channel Secret
access_token = 't5aeGlq0ECw8Kc0D66THVk0KDwsX6hu21GGWaAwRo635OjRbtfzJ1/sdiWcUrr2g6sMNuRCW6VtCsYiS2MUgYLv5lJ2hCExREwBt3IgnhVbPaFgoi87y/GdiHfZhf+trP+h1kyTQ0HQHoURFwGYhTwdB04t89/1O/w1cDnyilFU='
secret = '41e777e00598a08a03e037820e0e0803'

# 請將此處替換為您的 API 圖片上傳端點和用戶註冊資料端點
# upload_image_url = 'https://yourapi.com/upload_image'
# user_book_url = 'https://yourapi.com/api/books/'
# user_data_url = 'https://yourapi.com/api/users/'
# sign_up_user = 'https://yourapi.com/api/users/'
user_book_url = 'https://a102-61-220-37-156.ngrok-free.app/api/books/'
user_data_url = 'https://a102-61-220-37-156.ngrok-free.app/api/users/'
sign_up_user = 'https://a102-61-220-37-156.ngrok-free.app/api/users/'
book_interest = 'https://a102-61-220-37-156.ngrok-free.app/api/questionnaire_users_interests/'
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
waiting_for_search_keyword_response = False
waiting_for_book_detail_response = False
cart = []
waiting_for_add_to_cart_response = False  # 新增這行
current_book_for_cart = None  # 新增這行


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
    global waiting_for_search_keyword_response
    global waiting_for_book_detail_response
    global waiting_for_add_to_cart_response

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
    elif registration_state == 1: 
        try:
            user_data = validation(user_data_url)  # 使用 validation 函式驗證獲取使用者資料的請求
            if user_data:
                email = msg.strip()
                if check_email(user_data, email) or not re.match(r"[^@]+@[^@]+\.[^@]+", email) or contains_special_character(email) ==True:
                    reply_text = '該電子郵件地址已被使用或格式錯誤，請重新輸入'
                else:
                    reply_text = '請輸入您的使用者名稱：'
                    line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
                    registration_state += 1
                    registration_email = email
            else:
                reply_text = '無法連接到用戶資料伺服器，請檢查網路連接並稍後再試。'
        except requests.exceptions.RequestException as e:
            reply_text = '與伺服器通訊時發生錯誤，請稍後再試。'
        line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))

    # 處理用戶註冊流程
    elif registration_state == 2:  # 如果用戶註冊的狀態為 2
        try:
            user_data = validation(user_data_url)  # 使用 validation 函式獲取用戶資料
            if user_data:
                username = msg.strip()  # 獲取用戶輸入的使用者名稱

                if check_username(user_data, username) or len(username)<8 or contains_special_character(username) == True:  # 如果使用者名稱已存在
                    reply_text = '該使用者名稱已被使用或少於8個字符，請重新輸入'  # 提示用戶重新輸入
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
        if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or contains_special_character(password) ==True:
            reply_text = '密碼至少需要 8 個字符，並且至少包含一個大寫字母和一個小寫字母：'  # 提示用戶重新輸入
        else:
            registration_state = 0  # 歸零用戶註冊的狀態

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

    elif waiting_for_account:
        # 如果正在等待用戶輸入帳號
        account = msg.strip()  # 移除前後空格
        try:  
            if validation(user_data_url):
                user_data = validation(user_data_url)
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

     # 已經輸入了帳號，但尚未登入
    elif current_account is not None and not logged_in:
        #現在輸入密碼
        password = msg
        if validation(user_data_url):
            user_data = validation(user_data_url)
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
            if '搜尋' in msg:
                reply_text = '請輸入書籍關鍵字'
                line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
                waiting_for_search_keyword_response = True  # 設置等待用戶輸入關鍵字的標誌

            elif waiting_for_search_keyword_response:
                search_books(event, tk)  # 調用 search_books 函式，並將關鍵字傳遞過去
                waiting_for_search_keyword_response = False 

            elif '查詢書籍資料' in msg:
                reply_text = '請輸入書籍名稱'
                line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
                waiting_for_book_detail_response = True  # 設置等待用戶輸入書籍名稱的標誌

            elif waiting_for_book_detail_response:
                show_book_details(event, tk)
                waiting_for_book_detail_response = False

            elif '我的收藏' in msg:
                show_cart(tk)

            elif waiting_for_add_to_cart_response:
                handle_add_to_cart_response(event, tk, current_book_for_cart)
                waiting_for_add_to_cart_response = False
            elif '推薦' in msg:
                    user_id = current_account
                    user_interests = get_user_interest_by_id(user_id)
                    recommend_books_for_user(event, tk, user_book_url,user_interests)
                    line_bot_api.reply_message(tk,TextSendMessage(text=reply_text))
            elif '登出' in msg:
                logged_in = False
                reply_text = '已成功登出用戶帳號'
                line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
            
            else:
                #如果收到未知指令，回覆提示
                reply_text = "請輸入有效的指令，如：\n搜尋書籍\n查詢書籍詳細資料\n顯示收藏清單"
                line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))
                
        else:
            # 如果未登錄，直接回覆用戶輸入的訊息
            reply_text = '請先登入或註冊'
            line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))


# 定義函式用於新增用戶資料到 API
def register_user(username, password, email):
    data = {
        "username": username,
        "password": password,
        "email": email

    }

    try:
        if validation_return(sign_up_user, data):  # 调用 validation_return 函数来验证注册用户的请求
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(e)  # 請求異常，印出錯誤訊息
        return False  # 返回 False，表示註冊失敗


# 用於檢查帳號是否存在的函式
def check_account(user_data, account):
    for data in user_data:
        if account == str(data['username']):
            return True , account


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
    msg = event['message']['text']
    keyword = msg.lower()

    if validation(user_book_url):
        user_book_data = validation(user_book_url)

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
    msg = event['message']['text']
    book_name = msg.lower()  # 將用戶輸入的書名轉換為小寫字母

    if validation(user_book_url):
        user_book_data = validation(user_book_url)

        # 直接比較用戶輸入的書名與書籍列表中的書名
        for book in user_book_data:
            if book_name == book['title'].lower():
                # 找到匹配的書籍，構建詳細資訊的回覆訊息
                reply_text = f"書籍詳細資訊：\n"
                for key, value in book.items():
                    reply_text += f"\n{key}: {value}"
                reply_text += "\n\n請問您是否要將此書籍加入收藏? (請回覆'是'或'否')"
                line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))

                # 設置全域變數，用於標記正在等待用戶回覆加入購物清單的動作
                global waiting_for_add_to_cart_response
                waiting_for_add_to_cart_response = True

                # 記錄當前書籍詳細資訊，以便後續使用
                global current_book_for_cart
                current_book_for_cart = book

                return
        # 如果沒有找到匹配的書籍
        reply_text = "找不到指定名稱的書籍。"
    else:
        reply_text = '無法獲取書籍資料。'

    line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))

def show_cart(tk):
    global cart
    if len(cart) == 0:
        reply_text = "您的收藏清單是空的，請先選擇要收藏的書籍。"
    else:
        reply_text = "您已收藏的書籍清單如下：\n"
        for i, book in enumerate(cart, 1):
            reply_text += f"\n{i}. {book['title']} - 書籍ID：{book['book_id']}"
    line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))

def handle_add_to_cart_response(event, tk, current_book_for_cart):
    msg = event['message']['text']
    if msg == '是':
        # 將書籍添加到收藏中
        if add_to_cart(event, current_book_for_cart):  # 修改此行
            return
        else:
            reply_text = "抱歉，收藏已滿，無法再添加書籍。"
    elif msg == '否':
        # 用戶選擇不將書籍加入購物車
        reply_text = "已取消將書籍加入收藏。"
    else:
        # 用戶回覆無效
        reply_text = "請回覆'是'或'否'。"

    line_bot_api.reply_message(tk, TextSendMessage(text=reply_text))

def add_to_cart(event, current_book):
    global cart
    book = current_book
    if len(cart) < 5:
        cart.append(book)
        reply_text = f"《{book['title']}》已加入收藏。"
        line_bot_api.reply_message(event['replyToken'], TextSendMessage(text=reply_text))
        return True
    else:
        reply_text = "無法添加進收藏，請重新連接網路後。"
        line_bot_api.reply_message(event['replyToken'], TextSendMessage(text=reply_text))




def recommend_books_for_user(event, tk, user_book_url, user_ins): 
    # 根據使用者的喜好將書本過濾並依評分排序
    recommend_books = []
    user_book = validation(user_book_url)
    user_ins = random.sample(range(1, 11), 3)
    for ins in user_ins:
        book_list = [[book['title'], book['label'], book['average_rating']] for book in user_book if book['label'] == ins]
        recommend_books.append(sorted(book_list, key=lambda x: x[2]))
    
    recommend_number = 5

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
    sort_list = sorted(extra_list, key=lambda x: x[2])
    result.extend(sort_list[:extra_choose])
    
    # 將結果轉換為字串
    reply_text = '以下是推薦給您的書籍：\n\n'
    for i, book in enumerate(result, 1):
        reply_text += f"{i}. {book[0]}\n"

    
    return line_bot_api.reply_message(event['replyToken'], TextSendMessage(text=reply_text))

def validation(url):
    response =  requests.get(url) 
    if response.status_code == 200:
        jsonData = response.json()
        return  jsonData
def validation_return(url,data):
    response = requests.post(url, json=data) 
    if response.status_code == 201:
        return  True
    else:
        return False  # 如果註冊失敗，返回 False
    

def containsspecial_character(s):
    # 使用正則表達式來檢查是否包含特殊符號
    return bool(re.search(r"[^a-zA-Z0-9\u4e00-\u9fff]", s))
def contains_special_character(email):
    # 定義正則表達式，表示 email 只能包含字母、數字、點（.）和底線（）
    pattern = r'^[\w.-@]+$'
    # 使用 re.search() 函數進行匹配
    if re.search(pattern, email):
        return False  # 如果匹配成功，表示 email 中不包含特殊字符，返回 False
    else:
        return True  # 如果匹配失敗，表示 email 中包含特殊字符，返回 True

def user_register_data(sign_up_user, account):
    try:
        # 將 sign_up_user 參數通過 validation 函式進行驗證
        sign_up_user_ = validation(sign_up_user)
        
        # 將驗證後的 sign_up_user_ 賦值給 user_list
        user_list = sign_up_user_
        
        # 使用列表推導式從 user_list 中選擇符合帳戶名稱與提供的 account 參數相匹配的用戶
        user_id = [user["user_id"] for user in user_list if user_list['user_name'] == account]
        
        # 返回確認成功的布林值和用戶 ID
        return True, user_id[0]
    
    except Exception as e:
        # 如果出現異常，打印錯誤消息並返回失敗的布林值和空的用戶 ID
        print("An error occurred:", e)
        return False, None

def get_user_interest_by_id(user_id):
    try:
        interest =list( validation(book_interest))
        # print('xxxxxx     '+str(interest))
        interest_list = []
        for ins in interest:
            if ins['user_id'] == int(user_id):
                # print('---------------'+str(ins))
                interest_list.append(ins['interests_id'])
        # print('----------------'+list(set(interest_list)))
        return list(interest_list)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    app.run(debug=True)  # 在 debug 模式下運行 Flask 應用程式

