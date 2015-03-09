from flask import render_template, flash, redirect, url_for, request
from terUNIFI import app, db
from forms import CtrlForm
from unifi.controller import Controller


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
