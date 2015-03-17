from flask import render_template, flash, redirect, url_for, request, g
from terUNIFI import app, db
from forms import CtrlForm
from unifi.controller import Controller
from unifi.controllerv2 import ControllerV2
from unifi_control import ControllerV
from models import WifiCtrl, WifiAp, Location, WifiType, Company
from urlparse import urlparse



@app.route('/')
def index():
    return render_template('index.html')


# Testing Portals
@app.route('/guest/', methods=["GET", "POST"],
           defaults={'s':'0', 'unifi_site':''})
@app.route('/guest/<s>/<unifi_site>/', methods=["GET", "POST"])
def portal_unifi(s, unifi_site):
    ap_mac = request.args.get('ap')
    device = request.args.get('id')
    if WifiAp.query.filter_by(ap_mac=ap_mac).first():
        ap = WifiAp.query.filter_by(ap_mac=ap_mac).first_or_404()
        location = Location.query.get(ap.location_id)
        controller = WifiCtrl.query.get(ap.wifictrl_id)
        ctrl_type = WifiType.query.get(controller.type_id)
    else:
        if (s == 's'):
            controller = WifiCtrl.query.get(2)
            location = Location.query.get(2)
            ctrl_type = WifiType.query.get(controller.type_id)
        elif (s == '0'):
            controller = WifiCtrl.query.get(1)
            location = Location.query.get(1)
            ctrl_type = WifiType.query.get(controller.type_id)
    c = controller.connect()
    c.authorize_guest(device, 2, 500, 500, 1, ap_mac)
    print (
           "===============================",
           location,
           ap_mac
           )
    return redirect(url_for(
                    'welcome',
                    location_endpoint=location.endpoint,
                    **request.args
                    ))


@app.route('/welcome/<location_endpoint>/', methods=["GET", "POST"])
def welcome(location_endpoint):
    location = Location.query.filter_by(endpoint=location_endpoint).first()
    if location:
        return render_template(
                            '/locations/admixer.html',
                            location=location,
                            request=request.args
                                )
    else:
        print request.query_string
        return ('recieved {}'.format(request.query_string))



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
