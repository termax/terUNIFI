from flask import redirect, url_for, request
from . import guest
from .. import db
from ..models import WifiAp, Location, WifiCtrl, Device, Event
from terUNIFI import redis_store

import string
import random

def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Testing Portals
@guest.route(
    '/', methods=["GET"],
    defaults={'s': '0', 'unifi_site': ''}
            )
@guest.route('/<s>/<unifi_site>/', methods=["GET"])
def portal_unifi(s, unifi_site):
    # Decode args
    ap_mac = request.args.get('ap')
    dev_mac = request.args.get('id')
    url = request.args.get('url')
    ssid = request.args.get('ssid')
    ss = id_generator()
    # getting ap from db
    ap = WifiAp.get_by_mac(ap_mac)

    if ap is None:
        # add ap to db or return erro if no ap at controller
        for ctrl in WifiCtrl.query.all():
            ctrl.update_aps()
        print "APs updated"
        ap = WifiAp.get_by_mac(ap_mac)
        if ap is None:
            return 'ROUGE Access Point'

    # checking if the device is new or existing
    device = Device.get_or_create(dev_mac, ap_mac)
    dev = device.id
    # setting location by AP location
    location = Location.query.get(ap.location_id)
    # seting controller by AP
    controller = WifiCtrl.query.get(ap.wifictrl_id)

    # preathorizing client for 2 minutes
    c = controller.connect()
#    c.authorize_guest(dev_mac, 2, 500, 500, 5, ap_mac)
    print (
           "===============================",
           location,
           ap_mac
           )
    # Redis Session set
    ap_key = '{}/{}/ap_mac'.format(dev, ss)
    url_key = '{}/{}/url'.format(dev, ss)
    ss_key = 'sessions/{}/{}'.format(dev, ss)

    redis_store.setex(ss_key, ss, 3000)
    redis_store.setex(url_key, url, 3000)
    redis_store.setex(ap_key, ap_mac, 3000)
    redis_store.set('request', request.args)
    # packing request arg
    new_request = {'dev': dev, 'ss': ss}

#                  dict(
#                (name, eval(name)) for name in
#                [ss, dev]
#                        )
    print new_request
    return redirect(url_for(
                    'welcome.show',
                    location_endpoint=location.endpoint,
                    **new_request
                    ))
