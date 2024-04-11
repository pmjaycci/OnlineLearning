from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename  # secure_filename 함수 import 추가
from model.video import save_uploaded_file, allowed_file
from . import app
import os

video = Blueprint('video', __name__, url_prefix='/video')


@video.route('/')
def index():
    return render_template('index.html')


@video.route('/play/<filename>')
def play_video(filename):
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return render_template('index.html', filename=video_path)
