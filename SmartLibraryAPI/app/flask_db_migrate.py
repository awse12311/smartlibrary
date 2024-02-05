# 請執行下面指令進行資料庫回滾
# python db init
# python db migrate -m "Initial migration"
# python db upgrade





from flask import Flask
from flask_migrate import Migrate
from app.extensions import first_init_db
from app import create_app

app = create_app()

# 初始化 Flask-Migrate
migrate = Migrate(app, first_init_db)

if __name__ == '__main__':
    app.run()




