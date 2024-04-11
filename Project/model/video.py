import os

UPLOAD_FOLDER = 'uploads'

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}  # 허용할 파일 확장자 목록


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file):
    if file:
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return filename
    return None
