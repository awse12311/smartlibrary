# services/camera_service.py
from ..models.users import User, db
import cv2
import face_recognition
import numpy as np
from scipy.spatial import distance
from users_service import UserService

# 傳入鏡頭獲取的圖片(資料類型為npy陣列) 回傳辨識結果(臉部數量超過回傳-1 沒有搜尋到匹配者回傳-1 搜尋到匹配者回傳ID)
class CameraService:
    def __init__(self):
        self.face_rec_model = face_recognition.api.face_encodings
        self.face_embeddings = []
        self.database = {}
        self.update_embeddings()

    # embeddings更新資料
    def update_embeddings(self):
        try:
            self.database = UserService.get_all_users()
            self.face_embeddings = []
            for name in self.database["username"]:
                print("載入資料: " + name)
                self.face_embeddings.append(np.load("database/" + name + ".npy"))
        except Exception as e:
            raise e

    # 使用 face_recognition 獲取臉部嵌入
    def get_face_embedding(self, face_image):
        try:
            face_embedding = self.face_rec_model(face_image)
            # 如果沒有偵測到就回傳None
            return face_embedding[0] if len(face_embedding) > 0 else None
        except Exception as e:
            raise e
    
    # 計算兩個臉部embedding之間的餘弦相似度
    def cosine_similarity(self, embedding1, embedding2):
        try:
            return 1 - distance.cosine(embedding1, embedding2)
        except Exception as e:
            raise e
        
    # 從一組臉部embedding中找到最相似的臉
    def find_most_similar(self, target_embedding):
        try:
            # 求餘弦相似度
            similarities = [self.cosine_similarity(target_embedding, embedding) for embedding in self.face_embeddings]
            most_similar_index = np.argmax(similarities)
            most_similar_similarity = similarities[most_similar_index]
            print(similarities)
            if most_similar_similarity < 0.98: # 相似值超過98%則匹配成功
                return -1, 0
            return most_similar_index, most_similar_similarity
        except Exception as e:
            raise e

    # 捕捉其中一幀 檢測臉部並保存嵌入
    def recogintion_face(self, frame):
        try:
            # 將幀轉換為 RGB 格式（face_recognition 使用 RGB）
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 使用 face_recognition 獲取臉部位置
            face_locations = face_recognition.face_locations(rgb_frame)

            #frame = rgb_frame
            face_num = 0
            username = ""
            for face_location in face_locations:
                face_num += 1
                # 提取臉部位置座標（top, right, bottom, left）
                top, right, bottom, left = face_location

                # 從幀中裁剪臉部區域
                face_image = frame[top:bottom, left:right]
                face_embedding = self.get_face_embedding(face_image)

                # 若找到臉 則和資料庫中的配對
                if face_embedding is not None:
                    self.update_embeddings()
                    target = face_embedding 
                    id, score = self.find_most_similar(target)
                    if id == -1:
                        username = "無註冊資料"
                    else:
                        username = self.database["username"][id]
            if face_num == 0: # 沒有找到臉
                return 0, 0
            elif face_num > 1: # 超過一個臉
                return -1, 0
            elif username == "無註冊資料": # 找到臉但沒有匹配者
                return 1, face_image
            else: # 找到臉且已匹配
                return username, face_image
        except Exception as e:
            raise e

    # def create_user(data):
    #     try:
    #         user = User(**data)
    #         db.session.add(user)
    #         db.session.commit()
    #         return user
    #     except Exception as e:
    #         db.session.rollback()
    #         raise e
