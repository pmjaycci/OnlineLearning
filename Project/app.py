from controller.init import create_app

app = create_app()

app.secret_key = 'your_secret_key'  # 이 부분에 적절한 시크릿 키를 입력하세요.

if __name__ == '__main__':
    app.run(debug=True)

'''
project
├─ controller
│       ├─ account_controller.py
│       ├─ init.py
│       ├─ learn_add_controller.py
│       ├─ learn_detail_controller.py
│       ├─ main_controller.py
│       ├─ my_page_controller.py
│       └─ payment_controller.py
├─ model
│       ├─ account.py
│       ├─ database.py
│       ├─ learn_add.py
│       ├─ learn_detail.py
│       ├─ main.py
│       ├─ my_page.py
│       ├─ payment.py
│       └─ video.py
├─ static
│       └─ images
│               └─ bart.jpg
│       └─ videos
│               └─ sample_video.mp4
│ 
├─ templates
│       ├─ index.html
│       ├─ learn_add.html
│       ├─ learn_detail.html
│       ├─ my_page.html
│       └─ play.html
├─ app.py
├─ database.db
└─ schema.sql
'''
