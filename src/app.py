from flask import Flask
from flask import Response
from flask import render_template
from flask import abort


# from flask import Flask,render_template,  Response, request, redirect, url_for
# from flask_mail import Message
from flask_cors import CORS
# from flask_seeder import FlaskSeeder

from .config import app_config
from .models import db, bcrypt
# from .shared.Mailing import mail, Mailing
# from .shared import context
# from .shared.DdsStateManager import Context, InitialState, StateEventType

from .views.UserView import user_api as user_blueprint
# from .views.ActivityView import activity_api as activity_blueprint
# from .views.ConfigurationView import configuration_api as configuration_blueprint
# from .views.CameraControlView import camera_control_api as camera_control_blueprint
# from .views.VideoEngineView import video_engine_api as video_engine_blueprint
# from .views.CameraSequenceView import camerasequence_api as camerasequence_blueprint
# from .views.SectionView import section_api as section_blueprint
from .views.TransactionView import transaction_api as transaction_blueprint
# from .views.PhoneView import phone_api as phone_blueprint
# from .views.SnapScheduleView import snapschedule_api as snapschedule_blueprint
# from .views.ParameterView import parameter_api as parameter_blueprint
# from .views.FirmwareView import firmware_web as firmware_blueprint
from .views.LoginView import login_web as login_blueprint
# from .views.DeviceStatusView import device_status_api as device_status_blueprint
# from .views.DropboxView import dropbox_api as dropbox_blueprint


# import datetime
from datetime import datetime

from flask_login import LoginManager 
from .models.UserModel import UserModel, UserSchema
from time import sleep
# from flask_mail import Mail
# mail = Mail()
# import tensorflow as tf

# #initialize gpu
# tf.get_logger().setLevel('ERROR')           # Suppress TensorFlow logging (2)
# gpus = tf.config.experimental.list_physical_devices('GPU')
# for gpu in gpus:
#     tf.config.experimental.set_memory_growth(gpu, True)

# VERSION = '1.0.0.2'

def create_app(env_name):

    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(app_config[env_name])

    
    login_manager = LoginManager()
    login_manager.login_view = 'login_web.login'
    login_manager.init_app(app)

    # bcrypt.init_app(app)

    # mail.init_app(app)

    db.init_app(app)

    # context.init_app(app)

    # seeder = FlaskSeeder()
    # seeder.init_app(app, db)

    app.register_blueprint(user_blueprint, url_prefix='/api/auth')
    # app.register_blueprint(blogpost_blueprint, url_prefix='/api/v1/blogposts')
    # app.register_blueprint(payment_blueprint, url_prefix='/api/v1/payment')

    # app.register_blueprint(activity_blueprint, url_prefix='/api/activity')
    # app.register_blueprint(configuration_blueprint, url_prefix='/api/configuration')
    # app.register_blueprint(camera_control_blueprint, url_prefix='/api/camera')
    # app.register_blueprint(video_engine_blueprint, url_prefix='/api/videoEngine')
    # app.register_blueprint(camerasequence_blueprint, url_prefix='/api/camerasequences')
    # app.register_blueprint(section_blueprint, url_prefix='/api/sections')
    # app.register_blueprint(phone_blueprint, url_prefix='/api/phones')
    # app.register_blueprint(snapschedule_blueprint, url_prefix='/api/schedules')
    # app.register_blueprint(parameter_blueprint, url_prefix='/api/parameter')
    app.register_blueprint(transaction_blueprint, url_prefix='/api/transactions')
    
    # app.register_blueprint(device_status_blueprint, url_prefix='/api/status')
    # app.register_blueprint(dropbox_blueprint, url_prefix='/api/dropbox')

    app.register_blueprint(login_blueprint)
    # app.register_blueprint(firmware_blueprint)
    


    # context.processEvent(StateEventType.INIT)
    # context.processEvent(StateEventType.AUTO_START)

    # @app.route('/')
    # def index():
    #     current_mode = context._database.get_movement_method()
    #     mode_list = ['Static', 'Random', 'Sequence']
        
    #     return render_template('index.html',
    #                            mode_list=mode_list, 
    #                            current_mode = current_mode,
    #                            app_version = VERSION
    #                            )

    @app.route('/api/video')
    def video_detection():
        return Response(context._videoEngine.showOutputDetection(), mimetype='multipart/x-mixed-replace; boundary=frame')

    # @app.route('/video_display')
    # def video_display():
    #     return Response(context._videoEngine.showOutputDisplay(), mimetype='multipart/x-mixed-replace; boundary=frame')


    # authorization

    @app.route('/logStream')
    def stream():
        # datetime.strftime("%Y%m%d%H%M%S")
        logdate = datetime.now().strftime("%Y-%m-%d")
        def generate():
            with open('logs/' + logdate + '.log') as f:
                while True:
                    yield f.read()
                    sleep(1)

        return app.response_class(generate(), mimetype='text/plain')

    # @app.route('/about/')
    # def about():
    #     return render_template('about.html')

    # @app.route('/comments/')
    # def comments():
    #     comments = ['This is the first comment.',
    #                 'This is the second comment.',
    #                 'This is the third comment.',
    #                 'This is the fourth comment.'
    #                 ]

    #     return render_template('comments.html', comments=comments)

    # @app.route('/')
    # def hello():
    #     return render_template('index.html', utc_dt=datetime.datetime.utcnow())

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return UserModel.get_one_user(int(user_id))
    

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
    
    # @app.route('/messages/<int:idx>')
    # def message(idx):
    #     messages = ['Message Zero', 'Message One', 'Message Two']
    #     try:
    #         return render_template('message.html', message=messages[idx])
    #     except IndexError:
    #         abort(404)

    # @app.route('/profile')
    # def profile():
    #     return render_template('profile.html')

    # @app.route('/login')
    # def login():
    #     return render_template('login.html')

    # @app.route('/signup')
    # def signup():
    #     return render_template('signup.html')

    # @app.route('/logout')
    # def logout():
    #     return 'Logout'

    return app
