from flask import render_template, flash, redirect, url_for, request
from terUNIFI import app, db
from forms import CtrlForm
from unifi.controller import Controller
from models import WifiCtrl, WifiAp, Location


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
        return render_template('ctrl-view.html', ctrl_data=c)
    return render_template('ctrl.html', form=form)


# Testing Portals
@app.route('/guest/s/default/')
def reroute():
    return redirect('/portal/portal3')


@app.route('/portal/<ctrl_endpoint>/', methods=["GET", "POST"])
def portal(ctrl_endpoint):
    wifi_ctrl = WifiCtrl.query.filter_by(endpoint=ctrl_endpoint).first_or_404()
    ctrl_args_ap = request.args.get('ap')
    ctrl_args = request.query_string
    ap = WifiAp.query.filter_by(ap_mac=ctrl_args_ap)\
        .first_or_404()
    location = Location.query.get(ap.location_id).first_or_404()
    return ("Trying to access Controller {} and ap mac is {} <br>AP {} <br> {} <br> {} <br> {}"
            .format(wifi_ctrl.id, ctrl_args_ap, ap.location_id, location.
                    admixer_id, ctrl_args))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
