import json

class DataSave:

    def __init__(self):
        self.database = {}

    # json抓資料
    def load_data(self):
        with open('user_data.json', mode='r', encoding ='utf8') as jfile:
            self.database = json.load(jfile)
        return self.database
    
    # json放資料
    def save_and_reload_data(self, data):
        with open('user_data.json', mode='w', encoding ='utf8') as jfile:
            json.dump(data, jfile, indent =4)
        self.database = self.load_data()
        return
    
if __name__ == "__main__":
    datasave = DataSave()
    data = datasave.load_data()
    print(data)
    data["save"].append({"user":"456", "book_id":3})
    datasave.save_and_reload_data(data=data)
    print(data)