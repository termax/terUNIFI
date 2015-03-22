from flask import render_template, url_for, request
from . import welcome
from .. import db
from ..models import Location, Admixer
from terUNIFI import redis_store



@welcome.route('/<location_endpoint>/', methods=["GET"])
def show(location_endpoint):
    # Setting Location
    location = Location.query.filter_by(endpoint=location_endpoint).first()
    # Decoding request arguments
    dev = request.args.get('dev')
    ss = request.args.get('ss')

    if (location.admixer_id):
        admixer = Admixer.query.get(location.admixer_id)
    else:
        admixer = Admixer.query.get(1)
    if location:
        return render_template(
                            '/locations/admixer.html',
                            location=location,
                            admixer=admixer,
                            ss=ss,
                            dev=dev
                                )
    else:
        print request.query_string
        return ('NO Location \n', 'recieved {}'.format(request.query_string))
