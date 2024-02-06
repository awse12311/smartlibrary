from app import create_app

app = create_app()

if __name__ == '__main__':
    # 在debug模式下運行Flask應用程序
    app.run(debug=True)
