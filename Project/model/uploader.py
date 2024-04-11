import os
from flask import current_app
from werkzeug.utils import secure_filename


class Uploader:
    def allowed_image(filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def allowed_video(filename):
        """업로드된 파일이 허용된 동영상 파일인지 확인합니다."""
        allowed_extensions = {'mp4', 'avi', 'mov', 'mkv'}  # 허용할 동영상 확장자 목록
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    def upload_image(video):

        if video and Uploader.allowed_file(video.filename):
            # 파일을 저장할 경로 설정 (static/videos 디렉토리에 저장)

            video_name = video.filename
            path = current_app.config['UPLOAD_VIDEO']
            # 파일 저장
            video.save(os.path.join(path, secure_filename(video_name)))
        else:
            pass
        return

    def upload_video(file):
        pass

    pass
