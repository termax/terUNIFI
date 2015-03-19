from flask import redirect, url_for, request
from . import guest
from .. import db
from ..models import WifiAp, Location, WifiCtrl


# Testing Portals
@guest.route(
    '/', methods=["GET"],
    defaults={'s': '0', 'unifi_site': ''}
            )
@guest.route('/<s>/<unifi_site>/', methods=["GET"])
def portal_unifi(s, unifi_site):
    ap_mac = request.args.get('ap')
    device = request.args.get('id')
    print '################', ap_mac
    print WifiAp.query.filter_by(ap_mac=ap_mac).first()
    if WifiAp.query.filter_by(ap_mac=ap_mac).first():
        ap = WifiAp.query.filter_by(ap_mac=ap_mac).first_or_404()
        location = Location.query.get(ap.location_id)
        controller = WifiCtrl.query.get(ap.wifictrl_id)
        print '!!!!!!!!! AP:', ap
        print '!!!!!!!!! LOC:', location
    else:
        if (s == 's'):
            controller = WifiCtrl.query.get(2)
            location = Location.query.get(2)
            print '!!!!!!!!!???? LOC:', location
        elif (s == '0'):
            controller = WifiCtrl.query.get(1)
            location = Location.query.get(1)
            print '!!!!!!!!!$$$$ LOC:', location
    c = controller.connect()
    c.authorize_guest(device, 2, 500, 500, 1, ap_mac)
    print (
           "===============================",
           location,
           ap_mac
           )
    return redirect(url_for(
                    'welcome.show',
                    location_endpoint=location.endpoint,
                    **request.args
                    ))
