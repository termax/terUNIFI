from flask import render_template, flash, redirect, url_for, request
from terUNIFI import app, db

@app.route('/')
def index():
    return ('Hello World')

@app.route('/test')
def test():
    return('Test')

@app.route('/connect', methods=['GET'])
def connect():
    client = request.args
    for i in client:
        print ('{} arg: {}'.format(i, client[i]))
    return ('done')

