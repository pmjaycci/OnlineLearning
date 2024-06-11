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
    # 구매 내역
    sql = "SELECT * FROM buy_online_learn WHERE user_id = ?"
    buy_rows = Database.read_all_db(sql, user_id)
    # 구매 강의 목록
    buy_learn_rows = get_buy_learn_rows(buy_rows)
    buy_learn_videos_rows = get_buy_learn_videos_rows(buy_rows)
    # 판매 내역
    sql = "SELECT * FROM sell_online_learn WHERE user_id = ?"
    sell_rows = Database.read_all_db(sql, user_id)

    # 등록 강의 목록
    sql = "SELECT id, price, title FROM online_learn WHERE user_id = ?"
    learn_rows = Database.read_all_db(sql, user_id)

    # 등록 강의 학습 목록
    upload_rows = {}
    sql = "SELECT online_learn_id, learn_order, learn_name FROM online_learn_video WHERE user_id = ?"
    video_rows = Database.read_all_db(sql, user_id)

    for video_row in video_rows:
        id = video_row["online_learn_id"]

        if id not in upload_rows:
            upload_rows[id] = []

        upload_rows[id].append(video_row)

    return render_template('my_page.html', user_id=user_id,
                           buy_rows=buy_rows, buy_learn_rows=buy_learn_rows, buy_learn_videos_rows=buy_learn_videos_rows,
                           sell_rows=sell_rows,
                           learn_rows=learn_rows, upload_rows=upload_rows)


def get_buy_learn_rows(buy_rows):
    online_learn_ids = [row["online_learn_id"] for row in buy_rows]

    # online_learn_ids 리스트가 비어있으면 아무 작업도 하지 않음
    if not online_learn_ids:
        return

    sql = f"SELECT * FROM online_learn WHERE id IN ({
        ','.join(map(str, online_learn_ids))})"
    print(f"BUY LEARN ROWS SQL ==> {sql}")
    rows = Database.read_all_db(sql)
    return rows


def get_buy_learn_videos_rows(buy_rows):

    # online_learn_id 값들을 리스트로 추출
    online_learn_ids = [row["online_learn_id"] for row in buy_rows]

    # online_learn_ids 리스트가 비어있으면 아무 작업도 하지 않음
    if not online_learn_ids:
        return

    # SQL 쿼리 생성: online_learn_id 값들을 IN 연산자로 사용
    sql = f"SELECT * FROM online_learn_video WHERE online_learn_id IN ({
        ','.join(map(str, online_learn_ids))})"

    # 데이터베이스에서 결과 조회
    rows = Database.read_all_db(sql)

    # 결과 출력
    upload_rows = {}
    for row in rows:
        print(f"ONLINE LEARN VIDEO ==> learn_id [{
              row['online_learn_id']}] learn_name [{row['learn_name']}]")
        id = row["online_learn_id"]

        if id not in upload_rows:
            upload_rows[id] = []
        upload_rows[id].append(row)

    return upload_rows


@my_page.route('/upload_video', methods=['POST'])
def upload_video():
    user_id = session.get("user_id", "")
    if not user_id:
        return redirect(url_for('login'))  # 로그인이 필요한 경우 로그인 페이지로 리다이렉트

    if 'file' not in request.files:
        return "No file part"
    online_learn_id = request.form.get('learn_id')
    learn_name = request.form.get('learn_name')
    video = request.files['file']
    if video.filename == '':
        return "No selected file"
    if video and MyPage.allowed_file(video.filename):
        # 파일을 저장할 경로 설정 (static/videos 디렉토리에 저장)

        video_name = video.filename
        path = current_app.config['UPLOAD_VIDEO']

        sql = "SELECT MAX(learn_order) FROM online_learn_video WHERE user_id = ? AND online_learn_id = ?"
        row = Database.read_once_db(sql, user_id, online_learn_id)

        if row is None or row['MAX(learn_order)'] is None:
            learn_order = 1
        else:
            learn_order = row['MAX(learn_order)'] + 1

        sql = "INSERT INTO online_learn_video (user_id, online_learn_id, learn_order, learn_name, video_name) VALUES (?,?,?,?,?)"
        Database.write_db(sql, user_id, online_learn_id,
                          learn_order, learn_name, video_name)
        # 파일 저장
        video.save(os.path.join(path, secure_filename(video_name)))

        # 파일 업로드 후 마이페이지로 리다이렉트
        return redirect(url_for('my_page.index'))

    return "Invalid file format or file upload failed"


@my_page.route('/update_upload_video', methods=['POST'])
def update_upload_video():
    online_learn_id = request.form.get('learn_id')
    learn_name = request.form.get('learn_name')
    learn_order = request.form.get('learn_order')

    if learn_name == "" or 'file' not in request.files:
        return redirect(url_for('my_page.index'))

    video = request.files['file']
    video_name = video.filename
    if video_name == "":
        return redirect(url_for('my_page.index'))

    user_id = session.get("user_id", "")
    if not user_id:
        return redirect(url_for('login'))  # 로그인이 필요한 경우 로그인 페이지로 리다이렉트

    sql = "SELECT video_name FROM online_learn_video WHERE user_id = ? AND online_learn_id = ? AND learn_order = ?"
    row = Database.read_once_db(sql, user_id, online_learn_id, learn_order)
    print(f"TEST FileName [{row['video_name']}]")

    path = current_app.config['UPLOAD_VIDEO']
    delete_video = row['video_name']
    delete_path = os.path.join(path, delete_video)

    if delete_file(delete_path):
        print("Delete Success")
    else:
        print("Delete Fail")

    sql = "UPDATE online_learn_video SET learn_name = ?, video_name = ? WHERE user_id = ? AND online_learn_id = ? AND learn_order = ?"
    Database.write_db(sql, learn_name, video_name, user_id,
                      online_learn_id, learn_order)

    # 파일 저장
    video.save(os.path.join(path, secure_filename(video_name)))

    return redirect(url_for('my_page.index'))


@my_page.route('/delete_upload_video', methods=['POST'])
def delete_upload_video():
    online_learn_id = request.form.get('learn_id')
    learn_order = request.form.get('learn_order')

    user_id = session.get("user_id", "")
    if not user_id:
        return redirect(url_for('login'))  # 로그인이 필요한 경우 로그인 페이지로 리다이렉트

    sql = "SELECT video_name FROM online_learn_video WHERE user_id = ? AND online_learn_id = ? AND learn_order = ?"
    row = Database.read_once_db(sql, user_id, online_learn_id, learn_order)

    path = current_app.config['UPLOAD_VIDEO']
    delete_video = row['video_name']
    delete_path = os.path.join(path, delete_video)

    if delete_file(delete_path):
        print("Delete Success")
    else:
        print("Delete Fail")

    sql = "DELETE FROM online_learn_video WHERE user_id = ? AND online_learn_id = ? AND learn_order = ?"
    Database.write_db(sql, user_id, online_learn_id, learn_order)

    return redirect(url_for('my_page.index'))


def delete_file(file_path):
    try:
        # 파일 삭제
        os.remove(file_path)
        print(f"File deleted successfully: {file_path}")
        return True
    except OSError as e:
        print(f"Error deleting file: {e}")
        return False
