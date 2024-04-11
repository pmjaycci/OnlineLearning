
class MyPage:
    @staticmethod
    def allowed_file(filename):
        """업로드된 파일이 허용된 동영상 파일인지 확인합니다."""
        allowed_extensions = {'mp4', 'avi', 'mov', 'mkv'}  # 허용할 동영상 확장자 목록
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
