import pandas as pd
import requests
import json
import time
# 讀取CSV文件
df = pd.read_csv('SQL_TABLE\\books.csv')

# 將DataFrame轉換為JSON格式
json_data = df.to_json(orient='records')

# 定義API端點的URL
api_url = 'https://a102-61-220-37-156.ngrok-free.app/api/books/'

# 將JSON數據解析為列表
data_list = json.loads(json_data)

# 發送POST請求將JSON數據發送到API端點

for data in data_list[2795:]:
    time.sleep(0.5)
    response = requests.post(api_url, json=data)
    # 檢查請求是否成功
    if response.status_code == 201:
        print(f'成功發送數據：{data}')
    else:
        print(f'發送數據失敗：{data}，錯誤代碼：{response.status_code}')