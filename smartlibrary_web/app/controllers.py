#from app import db
#from app.models import User
from flask import render_template,Response,Blueprint,redirect, url_for,request,jsonify
from app.models import face_encoding
from .services.login_service import LoginService
from .services.camera_service import CameraService
from .services.recommend_service import RecommendService
from .services.fetch_data_service import FetchService
import base64
# 創建一個 Blueprint 實例
#from app import db
import asyncio
# flask import


closed = False

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    # 渲染名為 'index.html' 的模板並返回
    return render_template('index.html')

@bp.route('/register')
def register():
    # 渲染名為 'register.html' 的模板並返回
    return render_template('register.html')

@bp.route('/user/<userid>/')
def user(userid):
    userdata = FetchService().get_user_by_id(user_id=int(userid))
    print(userdata)
    # 利用回傳的ID獲得使用者的喜好清單
    user_ins = FetchService().get_user_interest_by_id(user_id=int(userid))
    # 利用喜好清單獲得推薦書籍的列表
    recommend_list = RecommendService().recommend_books_for_user(user_ins=user_ins)
    print(recommend_list)
    # 渲染名為 'user.html' 的模板並返回
    return render_template('user.html',  userid=userid , userdata=userdata, recommend_list=recommend_list)

@bp.route('/recommend')
def recommend():
    # 渲染名為 'recommend.html' 的模板並返回
    return render_template('recommend.html')

@bp.route('/borrow')
def borrow():
    # 渲染名為 'borrow.html' 的模板並返回
    return render_template('borrow.html')

@bp.route('/api/stream')
def video_stream():
    global closed
    closed = False
    # 設定人臉辨識主體(input_from為來源 如果要改成鏡頭就改0 影片則填入名稱)
    face = face_encoding(input_from = 0)
    return Response(face.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@bp.route('/api/closed_video')
def closed_video_stream():
    global closed
    closed = True
    asyncio.sleep(1)
    return redirect(url_for('routes.register'))

@bp.route('/opencv.js')
def opencv():
    return render_template('opencv.js')

@bp.route('/haarcascade_frontalface_default.xml')
def haarcascade_frontalface_default():
    return render_template('haarcascade_frontalface_default.xml')

@bp.route('/utils.js')
def utils():
    return render_template('utils.js')
# --------------------------------------------------------------------------------------------------------

    
# 存登入拍照圖片的函数
@bp.route('/save_image', methods=['POST'])
def save_image():
    # 從 POST 請求獲取圖片資料的 base64 編碼字串
    image_data_base64 = request.json.get('image')
    # print('--------------------------------------------')
    # print(image_data_base64)
    image_data_base64 = image_data_base64.split(',')[-1]
    # print('--------------------------------------------')
    # print(image_data_base64)
    try:
        # 解碼 base64 編碼的圖像數據为 bytes
        # 將圖像數據保存到文件
        with open('smartlibrary_web\database\login_temp.png', 'wb') as f:
            f.write(base64.b64decode(image_data_base64))
        # 返回成功的 HTTP 狀態碼
        return '', 200
    except Exception as e:
        print("Error occurred:", e)
        import traceback
        traceback.print_exc()
        return str(e), 500
    

# 註冊的函式
@bp.route('/registe', methods=['POST'])
def registe():
    email = request.json.get('email')
    password = request.json.get('password')
    booktype = request.json.get('booktype')
    username = request.json.get('username')
    print(booktype)
    print(email)
    check, register_result = LoginService.user_register(email=email, password=password, username=username, booktype=booktype)
    if check:
        # book_recommend = RecommendService.recommend_books_for_user(user_ins=booktype)
        return '',200
    else:
        print(register_result)
        return register_result,400
    # if check:
    #     print(f'註冊成功 會員ID為 {register_result}')
    # else:
    #     print(f'註冊失敗 原因 {register_result}')

    # 在這裡進行登入驗證和相應的處理

    # 返回成功的 HTTP 狀態碼

@bp.route('/check_face', methods=['POST'])
def check_face():
    result = CameraService().recogintion_face_for_image()
    if result == "no_face":
        return result,401
    elif result == "no_register":
        return result,200
    elif result == "over_face":
        return result,402
    else:
        return result,403

@bp.route('/login_face', methods=['POST'])
def login_face():
    # 使用暫存檔的圖片做人臉識別登入
    check, result = LoginService().user_login_with_face()
    if check:
        # 回傳登入結果(True/False), 使用者ID
        return jsonify({'success': True, 'user': result}),200
    return jsonify({'success': False, 'user': result}),401

@bp.route('/login', methods=['POST'])
def login():
    # 從 POST 請求中獲取用戶名和密碼
    email = request.json.get('email') #把前面的user改成email
    password = request.json.get('password')
    check, login_result = LoginService.user_login_check(email=email, password=password)

    # 在這裡進行登入驗證和相應的處理
    # 在後端終端中列印用戶名和密碼並回傳http回應的狀態碼
    if check:
        print(f'登入成功 歡迎 {login_result["username"]}')
        
        return jsonify({'success': True, 'user': login_result}), 200
    else:
        print(f'登入失敗 原因 {login_result}')
        return jsonify({'success': False, 'user': login_result}), 401