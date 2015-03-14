from flask import render_template, flash, redirect, url_for, request
from terUNIFI import app, db
from forms import CtrlForm
from unifi.controller import Controller
from unifi.controllerv2 import ControllerV2
from unifi_control import ControllerV
from models import WifiCtrl, WifiAp, Location, WifiType, Company
from urlparse import urlparse
from time import sleep


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return('Test')


@app.route('/connect', methods=['GET'])
def connect():
    client = request.args
    for i in client:
        print ('{} arg: {}'.format(i, client[i]))
    return ('done')


# Testing Unifi Controller
@app.route('/ctrl', methods=['GET', 'POST'])
def ctrl():
    form = CtrlForm()
    if form.validate_on_submit():
        url = form.url.data
        usr = form.usr.data
        pwd = form.pwd.data
        ver = form.ver.data
        c = Controller(url, usr, pwd, ver)
        return render_template('ctrl-view.html', ctrl1_data=c)
    return render_template('ctrl.html', form=form)


# Adding aps to db
@app.route('/ctrl-add')
def ctrl_add():
    ctrlrs_aps = []
    company = Company.query.get(1)
    print company
    ctrl = company.wifictrls[1]
    print ctrl
    c = ControllerV(ctrl.url, ctrl.usr, ctrl.pwd, ctrl.port, ctrl.ver)
    ctrlrs_aps.append(c.get_aps())
    ctrl = company.wifictrls[2]
    print ctrl
    c = ControllerV(ctrl.url, ctrl.usr, ctrl.pwd, ctrl.port, ctrl.ver)
    ctrlrs_aps.append(c.get_aps())
    return render_template('ctrl-view.html', ctrl_data=ctrlrs_aps)


# Testing Portals
@app.route('/guest/s/default/', methods=["GET", "POST"])
def portalv3():
    ap_mac = request.args.get('ap')
    device = request.args.get('id')
    ctrl_args = request.query_string
    ap = WifiAp.query.filter_by(ap_mac=ap_mac)\
        .first_or_404()
    location = Location.query.get(ap.location_id)
    controller = WifiCtrl.query.get(ap.wifictrl_id)
    ctrl_type = WifiType.query.get(controller.type_id)
    print controller.url, controller.usr, controller.pwd
    c = Controller(controller.url, controller.usr, controller.pwd,
                   controller.port, 'v{}'.format(floor(ctrl_type.firmware)))
    c.authorize_guest(device, 1, 500, 500, 500, ap_mac)
#    c.restart_ap(ap_mac)c.authorize_guest(device, "1", ap_mac)
    return ("Device {}, is connected to AP: {} at Location: {} and \
            Controller: {} ver {} <br><br> {}"
            .format(device, ap.name, location.name,
                    controller.name, ctrl_type.firmware, ctrl_args))


@app.route('/guest/', methods=["GET", "POST"])
def portalv2():
    ap_mac = request.args.get('ap')
    device = request.args.get('id')
    ctrl_args = request.query_string
    ap = WifiAp.query.filter_by(ap_mac=ap_mac)\
        .first_or_404()
    location = Location.query.get(ap.location_id)
    controller = WifiCtrl.query.get(ap.wifictrl_id)
    ctrl_type = WifiType.query.get(controller.type_id)
    print controller.url, controller.usr, controller.pwd
    c = ControllerV2(controller.url, controller.usr, controller.pwd,
                   controller.port, 'v{}'.format(floor(ctrl_type.firmware)))
    c.authorize_guest(device, 1, 500, 500, 500, ap_mac)
#    c.restart_ap(ap_mac)c.authorize_guest(device, "1", ap_mac)
    return ("Device {}, is connected to AP: {} at Location: {} and \
            Controller: {} ver {} <br><br> {}"
            .format(device, ap.name, location.name,
                    controller.name, ctrl_type.firmware, ctrl_args))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
