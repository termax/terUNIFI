from datetime import datetime

from terUNIFI import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'),
                           nullable=False)
    password_hash = db.Column(db.String)


# Company Can have many users
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.String(300))
    users = db.relationship('User', backref='company', lazy='dynamic')
    wifictrls = db.relationship('WifiCtrl', backref='company', lazy='dynamic')


class WifiType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    made_by = db.Column(db.String(80), nullable=False)
    firmware = db.Column(db.Float, nullable=False)
    wifictrls = db.relationship('WifiCtrl', backref='wifi_type',
                                lazy='dynamic')


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    endpoint = db.Column(db.String(10))
    description = db.Column(db.String(300))
    wifictrl_id = db.Column(db.Integer, db.ForeignKey('wifi_ctrl.id'),
                            nullable=False)
    wifi_aps = db.relationship('WifiAp', backref='location', lazy='dynamic')


class WifiCtrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(300))
    url = db.Column(db.String)
    usr = db.Column(db.String)
    pwd = db.Column(db.String)
    endpoint = db.Column(db.String(10))
    locations = db.relationship('Location', backref='wifi_ctrl',
                                lazy='dynamic')
    wifi_aps = db.relationship('WifiAp', backref='wifi_ctrl', lazy='dynamic')
    type_id = db.Column(db.Integer, db.ForeignKey('wifi_type.id'),
                        nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'),
                           nullable=False)


class WifiAp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    ap_mac = db.Column(db.String(20), unique=True)
    usite = db.Column(db.String(20))
    wifi_ctrl_id = db.Column(db.Integer, db.ForeignKey('wifi_ctrl.id'),
                             nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'),
                            nullable=False)
    events = db.relationship('Event', backref='wifi_ap',
                             lazy='dynamic')


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    ap_id = db.Column(db.Integer, db.ForeignKey('wifi_ap.id'),
                      nullable=False)
