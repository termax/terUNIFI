from flask import render_template, redirect, url_for, request
from . import connect
from .. import db
from ..models import WifiAp, Location, WifiCtrl
from terUNIFI import redis_store


@connect.route('/', methods=["GET"])
def connect():
    # Decoding request args
    ss = request.args.get('ss')
    dev = request.args.get('dev')

    # Redis Session keys
    ap_key = '{}/{}/ap_mac'.format(dev, ss)
    url_key = '{}/{}/url'.format(dev, ss)
    ss_key = 'sessions/{}/{}'.format(dev, ss)

    # Pulling redis session
    red_ss = redis_store.get(ss_key)
    red_ap = redis_store.get(ap_key)
    red_url = redis_store.get(url_key)

    # pull url from click if exists
    click_url = request.args.get('url')

    print ' !!! ', red_ss, ' !!! ', red_ap, ' !!! ', red_url
    if (red_ss == ss):
        if click_url:
            return redirect(click_url)
        return render_template(
                            '/locations/connect.html',
                            ss=ss,
                            dev=dev
                                )
    else:
        return 'Your Session has expired please start from the begining'
