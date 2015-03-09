from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class CtrlForm(Form):
    url = StringField('url', validators=[DataRequired()])
    usr = StringField('usr', validators=[DataRequired()])
    pwd = PasswordField('pwd', validators=[DataRequired()])
    ver = StringField('ver', validators=[DataRequired()])
