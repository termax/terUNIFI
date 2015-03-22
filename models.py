from datetime import datetime
from terUNIFI import db
from flask_login import UserMixin
from unifi_control import ControllerV


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'),
                           nullable=False)
    password_hash = db.Column(db.String)

    def __repr__(self):
        return '<Name: %r>' % self.username


# Company Can have many users
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.String(300))
    users = db.relationship('User', backref='company', lazy='dynamic')
    wifictrls = db.relationship('WifiCtrl', backref='company', lazy='dynamic')

    def __repr__(self):
        return '<Name: %r>' % self.name


class WifiType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    made_by = db.Column(db.String(80), nullable=False)
    firmware = db.Column(db.Float, nullable=False)
    wifictrls = db.relationship('WifiCtrl', backref='wifi_type',
                                lazy='dynamic')

    def __repr__(self):
        return '<Type: {}, v{}>'.format(self.made_by, self.firmware)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    endpoint = db.Column(db.String(10))
    description = db.Column(db.String(300))
    admixer_id = db.Column(db.Integer, db.ForeignKey('admixer.id'))
    wifictrl_id = db.Column(db.Integer, db.ForeignKey('wifi_ctrl.id'),
                            nullable=False)
    wifi_aps = db.relationship('WifiAp', backref='location', lazy='dynamic')

    @staticmethod
    def get_by_name(name):
        return Location.query.filter_by(name=name).first()

    def __repr__(self):
        return '<Name: %r>' % self.name


class WifiCtrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(300))
    url = db.Column(db.String)
    usr = db.Column(db.String)
    pwd = db.Column(db.String)
    port = db.Column(db.Integer)
    endpoint = db.Column(db.String(10))
    ver = db.Column(db.String(2))
    locations = db.relationship('Location', backref='wifi_ctrl',
                                lazy='dynamic')
    wifi_aps = db.relationship('WifiAp', backref='wifi_ctrl', lazy='dynamic')
    type_id = db.Column(db.Integer, db.ForeignKey('wifi_type.id'),
                        nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'),
                           nullable=False)

    def connect(self):
        return ControllerV(self.url, self.usr, self.pwd, self.port, self.ver)

    @staticmethod
    def connect_by_id(id):
        ctrl = WifiCtrl.query.filter_by(id=id).first()
        ctrl = ControllerV(ctrl.url, ctrl.usr, ctrl.pwd, ctrl.port, ctrl.ver)
        return ctrl

    def update_aps(self):
        c = self.connect()
        for ap in c.get_aps():
            ap_name = ap['name']
            loc = ap['name'].split()[0]
            db_ap = WifiAp.get_by_mac(ap['mac'])
            if Location.get_by_name(loc) is None:
                endpoint = loc.lower()
                add_loc = Location(
                    name=loc,
                    endpoint=endpoint,
                    wifictrl_id=self.id
                                        )
                db.session.add(add_loc)
                db.session.commit()
            if db_ap is None:
                add_ap = WifiAp(
                        name=ap['name'],
                        ap_mac=ap['mac'],
                        usite="default",
                        wifictrl_id=self.id,
                        location_id=Location.get_by_name(loc).id
                                 )
                db.session.add(add_ap)
                db.session.commit()
            elif (db_ap.name != ap_name):
                db_ap.name = ap['name']
                db_ap.wifictrl_id = self.id
                db_ap.location_id = Location.get_by_name(loc).id
                db.session.commit()

        return True

    def __repr__(self):
        return '<Name: %r>' % self.name


class WifiAp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    ap_mac = db.Column(db.String(20), unique=True)
    usite = db.Column(db.String(20))
    wifictrl_id = db.Column(db.Integer, db.ForeignKey('wifi_ctrl.id'),
                            nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'),
                            nullable=False)
    events = db.relationship('Event', backref='wifi_ap',
                             lazy='dynamic')

    @staticmethod
    def get_by_mac(mac):
        return WifiAp.query.filter_by(ap_mac=mac).first()

    def __repr__(self):
        return '<Name: %r>' % self.name


class Admixer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    loc_name = db.Column(db.String(120))
    ad_id = db.Column(db.String)
    z_id = db.Column(db.String)
    locations = db.relationship('Location', backref='admixer', lazy='dynamic')

    @staticmethod
    def get_by_name(name):
        return Admixer.query.filter_by(name=name).first()

    @staticmethod
    def get_by_loc_name(name):
        return Admixer.query.filter_by(loc_name=name).first()

    def __repr__(self):
        return '<Name: %r>' % self.name


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_mac = db.Column(db.String(20), unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now)
    last_seen = db.Column(db.DateTime, default=datetime.now)
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_type.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    events = db.relationship('Event', backref='device', lazy='dynamic')

    @staticmethod
    def get_or_create(mac, ap):
        dev = Device.query.filter_by(device_mac=mac).first()
        wifiap = WifiAp.get_by_mac(ap)
        if dev is not None:
            print '!!!!!!!!!!!!!!!!!!', dev.id
            print '!!!!!!!!!!!!!!!!!!', wifiap.id
            dev.last_seen = datetime.now()
            event = Event(
                    ap_id=wifiap.id, device_id=dev.id,
                    event_type="Device Returned"
                            )
            db.session.add(dev)
            db.session.add(event)
            db.session.commit()
        else:
            print '!!!!!!!!!!!!!!!!!!NEW'
            dev = Device(device_mac=mac)
            db.session.add(dev)
            db.session.commit()
            print dev.id
            event = Event(
                    ap_id=wifiap.id, device_id=dev.id,
                    event_type="Device Created"
                            )
            db.session.add(event)
            db.session.commit()
        return dev

    def __repr__(self):
        return '<mac: %r>' % self.device_mac


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(80))
    pin = db.Column(db.Integer)
    pass_hash = db.Column(db.String)
    devices = db.relationship('Device', backref='client', lazy='dynamic')

    def __repr__(self):
        return '<username: %r>' % self.username


class DeviceType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    company = db.Column(db.String(120))
    model = db.Column(db.String(120))
    devices = db.relationship('Device', backref='device_type', lazy='dynamic')

    def __repr__(self):
        return '<name: %r>' % self.name


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    ap_id = db.Column(db.Integer, db.ForeignKey('wifi_ap.id'),
                      nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    event_type = db.Column(db.String)
    event_vars = db.Column(db.String)

    def __repr__(self):
        return '<Event: %r>' % self.id
