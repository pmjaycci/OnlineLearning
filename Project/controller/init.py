from flask import Flask
from controller.main_controller import main
from controller.learn_detail_controller import learn_detail
from controller.learn_add_controller import learn_add
from controller.my_page_controller import my_page
from controller.payment_controller import payment
from controller.video_controller import video
from model.database import Database
UPLOAD_IMAGE = 'static/images'
UPLOAD_VIDEO = 'static/videos'


def create_app():

    app = Flask(__name__, template_folder='../templates',
                static_folder="../static")
    app.config['UPLOAD_IMAGE'] = UPLOAD_IMAGE
    app.config['UPLOAD_VIDEO'] = UPLOAD_VIDEO
    app.register_blueprint(main)
    app.register_blueprint(learn_detail)
    app.register_blueprint(learn_add)
    app.register_blueprint(my_page)
    app.register_blueprint(payment)
    app.register_blueprint(video)
    with app.app_context():
        Database.init_db()
    return app
