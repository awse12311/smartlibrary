# services/camera_service.py
import cv2
import face_recognition
import numpy as np
from scipy.spatial import distance
from .fetch_data_service import FetchService

# 傳入鏡頭獲取的圖片(資料類型為npy陣列) 回傳辨識結果(臉部數量超過回傳-1 沒有搜尋到匹配者回傳-1 搜尋到匹配者回傳ID)
class CameraService:
    def __init__(self):
        self.login_temp_png = "smartlibrary_web\database\login_temp.png"
        self.login_temp_npy = "smartlibrary_web\database\login_temp.npy"
        self.face_rec_model = face_recognition.api.face_encodings
        self.face_embeddings = []
        self.database = []
        self.user_id_list = []
        self.frame = cv2.imread(self.login_temp_png)

    # embeddings更新資料
    def update_embeddings(self):
        try:
            origin_data = FetchService().get_all_users()
            self.database = []
            self.user_id_list = []
            self.face_embeddings = []
            for name in origin_data:
                username = name["username"]
                user_id = name["user_id"]
                self.database.append({"username":username, "user_id":user_id})
                try:
                    data = np.load("smartlibrary_web\database\\"+ str(user_id) + ".npy")
                    print(data)
                    self.face_embeddings.append(data)
                    self.user_id_list.append(user_id)
                    print("成功")
                except:
                    print("沒找到資料")
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
            print("找到最相似的臉")
            # 求餘弦相似度
            # 照順序對self.face_embeddings的list中所有資料做cosine_similarity 並存成一個新的list
            similarities = [self.cosine_similarity(target_embedding, embedding) for embedding in self.face_embeddings]
            # 用np.argmax找出新list中最大的位置(最相似)
            most_similar_index = np.argmax(similarities)
            # 將新list中最大位置的值拿出來
            most_similar_similarity = similarities[most_similar_index]
            most_similar_id = self.user_id_list[most_similar_index]
            print(similarities)
            # 如果最大值小於0.97 則代表沒有匹配成功 回傳-1
            if most_similar_similarity < 0.97: # 相似值超過98%則匹配成功
                return -1, 0
            # 若匹配成功 回傳ID和值
            return most_similar_id, most_similar_similarity
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
        self.update_embeddings()
        try:
            print("開始比對")
            frame = cv2.imread(self.login_temp_png)
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
                    target = face_embedding
                    # score為最高相似度
                    id, score = self.find_most_similar(target)
                    if id == -1:
                        user_id = -1
                    else:
                        user_id = id
                    print(user_id)
            if face_num == 0: # 沒有找到臉
                return "no_face"
            elif face_num > 1: # 超過一個臉
                return "over_face"
            elif user_id == -1: # 找到臉但沒有匹配者
                cv2.imwrite(self.login_temp_png, face_image)
                np.save(self.login_temp_npy, face_embedding)
                return "no_register"
            else: # 找到臉且已匹配
                cv2.imwrite(self.login_temp_png, face_image)
                np.save(self.login_temp_npy, face_embedding)
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
    
    def save_temp_to_data(self, user_id:str):
        # 讀取暫存檔的npy和jpg 並以ID命名後存到資料內.
        temp_npy = np.load("smartlibrary_web\database\login_temp.npy",allow_pickle=True)
        cv2.imwrite(f"smartlibrary_web\database\{user_id}.png", self.frame)
        np.save(f"smartlibrary_web\database\{user_id}.npy", temp_npy)

    # def create_user(data):
    #     try:
    #         user = User(**data)
    #         db.session.add(user)
    #         db.session.commit()
    #         return user
    #     except Exception as e:
    #         db.session.rollback()
    #         raise e
