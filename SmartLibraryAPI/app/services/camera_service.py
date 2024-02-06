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
        self.database = []
        self.update_embeddings()
        self.frame = cv2.imread("SmartLibraryAPI/app/content/temp/login_temp.png")

    # embeddings更新資料
    def update_embeddings(self):
        try:
            origin_data = UserService.get_all_users()
            self.database = []
            self.face_embeddings = []
            for name in origin_data:
                username = name["username"]
                user_id = name["user_id"]
                print("載入資料: " + user_id)
                self.database.append({"username":username, "user_id":user_id})
                self.face_embeddings.append(np.load("SmartLibraryAPI/app/content/source/npy/" + user_id + ".npy"))
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
            # 照順序對self.face_embeddings的list中所有資料做cosine_similarity 並存成一個新的list
            similarities = [self.cosine_similarity(target_embedding, embedding) for embedding in self.face_embeddings]
            # 用np.argmax找出新list中最大的位置(最相似)
            most_similar_index = np.argmax(similarities)
            # 將新list中最大位置的值拿出來
            most_similar_similarity = similarities[most_similar_index]
            print(similarities)
            # 如果最大值小於0.98 則代表沒有匹配成功 回傳-1
            if most_similar_similarity < 0.98: # 相似值超過98%則匹配成功
                return -1, 0
            # 若匹配成功 回傳位置和值
            return most_similar_index, most_similar_similarity
        except Exception as e:
            raise e

    # 傳入一個圖片 回傳是否有人臉在裡面
    def recogintion_face(self, frame):
        try:
            # 將幀轉換為 RGB 格式（face_recognition 使用 RGB）
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 使用 face_recognition 獲取臉部位置
            face_locations = face_recognition.face_locations(rgb_frame)
            for face_location in face_locations:
                return True
            return False
        except Exception as e:
            raise e

    # 捕捉其中一幀 檢測臉部並保存嵌入
    def recogintion_face_for_image(self):
        try:
            frame = self.frame
            # 將幀轉換為 RGB 格式（face_recognition 使用 RGB）
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 使用 face_recognition 獲取臉部位置
            face_locations = face_recognition.face_locations(rgb_frame)

            #frame = rgb_frame

            # 臉部記數
            face_num = 0
            user_id = -1
            for face_location in face_locations:
                face_num += 1
                # 提取臉部位置座標（top, right, bottom, left）
                top, right, bottom, left = face_location

                EXTRA_CUT = 30
                # 將裁剪區域擴大
                expanded_top = max(0, top - EXTRA_CUT)
                expanded_right = min(frame.shape[1], right + EXTRA_CUT)
                expanded_bottom = min(frame.shape[0], bottom + EXTRA_CUT)
                expanded_left = max(0, left - EXTRA_CUT)

                # 從幀中裁剪擴大後的臉部區域
                face_image = frame[expanded_top:expanded_bottom, expanded_left:expanded_right]
                face_embedding = self.get_face_embedding(face_image)

                # 若找到臉 則和資料庫中的配對
                if face_embedding is not None:
                    self.update_embeddings()
                    target = face_embedding
                    # score為最高相似度
                    id, score = self.find_most_similar(target)
                    if id == -1:
                        user_id = -1
                    else:
                        user_id = self.database[id]["user_id"]
            if face_num == 0: # 沒有找到臉
                return "no_face"
            elif face_num > 1: # 超過一個臉
                return "over_face"
            elif user_id == -1: # 找到臉但沒有匹配者
                cv2.imwrite("SmartLibraryAPI/app/content/temp/login_temp.jpg", face_image)
                np.save("SmartLibraryAPI/app/content/temp/login_temp.npy", face_embedding)
                return "no_register"
            else: # 找到臉且已匹配
                cv2.imwrite("SmartLibraryAPI/app/content/temp/login_temp.jpg", face_image)
                np.save("SmartLibraryAPI/app/content/temp/login_temp.npy", face_embedding)
                return user_id
        except Exception as e:
            raise e

    def recogintion_face_with_cascade(self, frame):
        try:
            face_cascade = cv2.CascadeClassifier("SmartLibraryAPI/app/content/temp/haarcascade_frontalface_default.xml")
            # 將幀轉換為 RGB 格式（face_recognition 使用 RGB）
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 使用 face_recognition 獲取臉部位置
            face_locations = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(150, 150))
            for (x, y, w, h) in face_locations:
                return True
            return False
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
