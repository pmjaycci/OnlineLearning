import os
from flask import Blueprint, current_app, redirect, render_template, request, session, url_for
from model.database import Database
from model.my_page import MyPage
from werkzeug.utils import secure_filename

my_page = Blueprint('my_page', __name__, url_prefix='/my_page')


@my_page.route('/', methods=['GET', 'POST'])
def index():
    user_id = ""
    if "user_id" in session:
        user_id = session.get("user_id")
    if user_id == "":
        pass
    sql = f"SELECT * FROM buy_online_learn WHERE user_id = ?"
    buy_rows = Database.read_all_db(sql, user_id)

    sql = f"SELECT * FROM sell_online_learn WHERE user_id = ?"
    sell_rows = Database.read_all_db(sql, user_id)

    return render_template('my_page.html', user_id=user_id, buy_rows=buy_rows, sell_rows=sell_rows)


@my_page.route('/upload_video', methods=['POST'])
def upload_video():
    user_id = session.get("user_id", "")
    if not user_id:
        return redirect(url_for('login'))  # 로그인이 필요한 경우 로그인 페이지로 리다이렉트

    if 'file' not in request.files:
        return "No file part"

    video = request.files['file']
    print(f'테스트: 파일명 : {video.filename}')
    if video.filename == '':

        return "No selected file"

    if video and MyPage.allowed_file(video.filename):
        # 파일을 저장할 경로 설정 (static/videos 디렉토리에 저장)

        video_name = video.filename
        path = current_app.config['UPLOAD_VIDEO']
        # 파일 저장
        video.save(os.path.join(path, secure_filename(video_name)))

        # 파일 업로드 후 마이페이지로 리다이렉트
        return redirect(url_for('my_page.index'))

    return "Invalid file format or file upload failed"
