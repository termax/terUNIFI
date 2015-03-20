import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext import wtf
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.superadmin import Admin, BaseView, expose, model


from .config import config_by_name
#basedir = os.path.abspath(os.path.dirname(__file__))

#app = Flask(__name__)



db = SQLAlchemy()

# Configure Admin
admin = Admin()


# Configure authentification
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"


# enable debugtoolbar
toolbar = DebugToolbarExtension()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    toolbar.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .guest import guest as guest_blueprint
    app.register_blueprint(guest_blueprint, url_prefix='/guest')

    from .welcome import welcome as welcome_blueprint
    app.register_blueprint(welcome_blueprint, url_prefix='/welcome')

    from .connect import connect as connect_blueprint
    app.register_blueprint(connect_blueprint, url_prefix='/connect')


# Flask Super Admin and vievs
    from .models import Company, User, WifiType, Location, WifiCtrl,\
        WifiAp, Event, Admixer, Device

    from .adminviews import CompanyModel, UserModel, LocationModel,\
        WifiTypeModel, WifiCtrlModel, WifiApModel, EventModel, AdmixerModel,\
        DeviceModel

    admin.register(Company, CompanyModel)
    admin.register(User, UserModel)
    admin.register(WifiType, WifiTypeModel)
    admin.register(Location, LocationModel)
    admin.register(WifiCtrl, WifiCtrlModel)
    admin.register(WifiAp, WifiApModel)
    admin.register(Event, EventModel)
    admin.register(Admixer, AdmixerModel)
    admin.register(Device, DeviceModel)

    return app
