from flask import render_template, redirect, url_for, request
from . import connect
from .. import db
from ..models import WifiAp, Location, WifiCtrl


@connect.route('/', methods=["GET"])
def connect():
    return 'connect'
