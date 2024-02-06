#from app import db
import cv2
import face_recognition
import numpy as np
import json
from scipy.spatial import distance
from PIL import ImageFont, ImageDraw, Image
from io import BytesIO
from PIL import Image

# import sys
# sys.path.append("/app/controllers")

class face_encoding:
    def __init__(self, input_from):
        self.face_rec_model = face_recognition.api.face_encodings
        self.face_embeddings = []
        self.database = {}
        self.input_from = input_from

    # embeddings更新資料
    def update_embeddings(self):
        self.face_embeddings = []
        for name in self.database["name"]:
            print(name)
            self.face_embeddings.append(np.load("database/" + name + ".npy"))

    # json抓資料
    def load_data(self):
        with open('data.json', mode='r', encoding ='utf8') as jfile:
            jdata = json.load(jfile)
        return jdata

    # json放資料
    def save_and_reload_data(self, data):
        with open('data.json', mode='w', encoding ='utf8') as jfile:
            json.dump(data, jfile, indent =4)
        self.database = self.load_data()
        return
    
    # 使用 face_recognition 獲取臉部嵌入
    def get_face_embedding(self, face_image):
        face_embedding = self.face_rec_model(face_image)
        # 如果沒有偵測到就回傳None
        return face_embedding[0] if len(face_embedding) > 0 else None
    
    # 計算兩個臉部embedding之間的餘弦相似度
    def cosine_similarity(self, embedding1, embedding2):
        return 1 - distance.cosine(embedding1, embedding2)
    
    # 從一組臉部embedding中找到最相似的臉
    def find_most_similar(self, target_embedding):
        # 求餘弦相似度
        similarities = [self.cosine_similarity(target_embedding, embedding) for embedding in self.face_embeddings]
        most_similar_index = np.argmax(similarities)
        most_similar_similarity = similarities[most_similar_index]
        print(similarities)
        if most_similar_similarity < 0.98:
            return -1, 0
        return most_similar_index, most_similar_similarity

    # 在圖像上放置文字(暫時沒有用)
    def put_text_on_image(self, img, text, position):
        # 定義字體的大小、顏色和粗細
        font_scale = 1.5
        color = (0, 255, 0)  # 綠色 (BGR 格式)
        thickness = 2
        cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness, cv2.LINE_AA)

    # 在圖像上繪製文字
    def draw_text(self, img, text, pos, font_size=20):
        b, g, r, a = 0, 255, 255, 0
        # 使用simsun中文字型
        fontpath = "simsun.ttc"
        font = ImageFont.truetype(fontpath, font_size)
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        draw.text(pos, text, font=font, fill=(b, g, r, a))
        img = np.array(img_pil)
        return img
    
    # 捕捉其中一幀 檢測臉部並保存嵌入
    def grab_face_and_save_embedding(self, cap):
        ret, frame = cap.read()

        # 將幀轉換為 RGB 格式（face_recognition 使用 RGB）
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 使用 face_recognition 獲取臉部位置
        face_locations = face_recognition.face_locations(rgb_frame)

        frame = rgb_frame
        for face_location in face_locations:
            # 提取臉部位置座標（top, right, bottom, left）
            top, right, bottom, left = face_location

            # 從幀中裁剪臉部區域
            face_image = frame[top:bottom, left:right]
            face_image_saved = frame[top-20:bottom+20, left-20:right+20]
            face_embedding = self.get_face_embedding(face_image)
            ### 這是原始版本的程式碼 需要改掉
            # # 如果按下 's' 鍵 保存臉部嵌入
            # if cv2.waitKey(1) & 0xFF == ord('s'):
            #     if face_embedding is not None:
            #         # 對臉部嵌入執行某些操作（例如，保存到文件）
            #         # 例如，可以按以下方式保存到文件：
            #         cv2.imshow("grab face_image", face_image_saved)
            #         # 註冊帳號和密碼 並回傳給資料庫
            #         register_name = input("請輸入你的姓名： ")
            #         register_password = input("請輸入你想設定的密碼： ")
            #         self.database["name"].append(register_name)
            #         self.database["password"].append(register_password)
            #         # 儲存臉部的.npy及.jpg檔
            #         np.save("database/" + register_name + ".npy", face_embedding)
            #         cv2.imwrite("database/" + register_name + ".jpg", face_image_saved)
            #         # 更新資料和embeddings
            #         self.save_and_reload_data(self.database)
            #         self.update_embeddings()

            # 繪製一個框框圍繞臉部
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # 若找到臉 則和資料庫中的配對
            if face_embedding is not None:
                target = face_embedding 
                id, score = self.find_most_similar(target)
                if id == -1:
                    frame = self.draw_text(frame, "無註冊資料", (left-20, top-20))
                else:
                    #put_text_on_image(frame, str(id), (left-20, top-20))
                    frame = self.draw_text(frame, self.database["name"][id], (left-20, top-20))
        # 最後將影像重新調整大小
        img_bytes = self.resize_img_2_bytes(frame, resize_factor=0.8, quality=30)
        return img_bytes

    # 主要運作function
    def gen_frames(self):
        
        # 設定影像來源
        cap = cv2.VideoCapture(self.input_from)
        # 更新資料庫
        self.database = self.load_data()
        self.update_embeddings()
        # 主要迴圈
        while True:
            from app.controllers import closed
            if closed:
                break
            # 將影像丟到grab_face_and_save_embedding處理後拿回成品(已經辨識好的)
            img_bytes = self.grab_face_and_save_embedding(cap=cap)
            if img_bytes:
                # 把處理後的影像丟到flask端
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')
    
    # 用BytesIO調整影像大小並去除多餘的資料
    def resize_img_2_bytes(self, image, resize_factor, quality):
        bytes_io = BytesIO()
        img = Image.fromarray(image)

        w, h = img.size
        img.thumbnail((int(w * resize_factor), int(h * resize_factor)))
        img.save(bytes_io, 'jpeg', quality=quality)
        
        return bytes_io.getvalue()

