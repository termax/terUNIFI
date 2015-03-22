from flask import render_template, url_for
from . import main
from terUNIFI import redis_store


@main.route('/')
def index():
    return 'Hello'

@main.route('redis/')
def redis_test():
    return redis_store.get('tomato')

@main.route('test', methods=['GET'])
def test():
    args = {
        'url': 1,
        'id': 2,
        'ap': 3
            }
    return url_for('.test', **args)

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
