import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext import wtf
from flask_debugtoolbar import DebugToolbarExtension

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


# Configure database
app.config['SECRET_KEY'] = \
    '\xcfA\xa2\xb52$*:c\xc2},E\x0f"\xb7\xc6\xc3\x1di\xc2\t\x93\xe6'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'terunifi.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)


# Configure authentification
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

# enable debugtoolbar
toolbar = DebugToolbarExtension(app)

from .guest import guest as guest_blueprint
app.register_blueprint(guest_blueprint, url_prefix='/guest')

from .welcome import welcome as welcome_blueprint
app.register_blueprint(welcome_blueprint, url_prefix='/welcome')

from .connect import connect as connect_blueprint
app.register_blueprint(connect_blueprint, url_prefix='/connect')

import models
import views
import admin
