from flask import Blueprint, current_app, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename  # secure_filename 함수 import 추가
from model.video import save_uploaded_file, allowed_file
import mimetypes
from model.database import Database
import os

video = Blueprint('video', __name__, url_prefix='/video')


@video.route('/')
def index():
    return render_template('test.html')


@video.route('/play', methods=['POST', 'GET'])
def play():
    online_learn_id = request.form.get('learn_id')
    learn_order = request.form.get('learn_order')
    user_id = request.form.get('user_id')

    sql = "SELECT video_name FROM online_learn_video WHERE user_id = ? AND online_learn_id = ? AND learn_order = ?"
    row = Database.read_once_db(sql, user_id, online_learn_id, learn_order)

    video_name = row['video_name']
    # video_path = os.path.join(current_app.config['UPLOAD_VIDEO'], video_name)
    video_path = f'videos/{video_name}'
    mime_type, _ = mimetypes.guess_type(video_path)

    print(f"LEARN ID[{online_learn_id}] ORDER[{
          learn_order}] USER ID[{user_id}] VIDEO NAME[{video_name}] PATH[{video_path}]")

    sql = "SELECT learn_order, learn_name, video_name FROM online_learn_video WHERE user_id = ? AND online_learn_id = ? AND learn_order != ?"
    video_rows = Database.read_all_db(
        sql, user_id, online_learn_id, learn_order)

    return render_template('play.html', video_path=video_path, mime_type=mime_type, video_rows=video_rows, online_learn_id=online_learn_id, user_id=user_id)
