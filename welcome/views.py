from flask import render_template, url_for, request
from . import welcome
from .. import db
from ..models import Location, Admixer


@welcome.route('/<location_endpoint>/', methods=["GET"])
def show(location_endpoint):
    location = Location.query.filter_by(endpoint=location_endpoint).first()
    if (location.admixer_id):
        admixer = Admixer.query.get(location.admixer_id)
    else:
        admixer = Admixer.query.get(1)
    if location:
        return render_template(
                            '/locations/admixer.html',
                            location=location,
                            admixer=admixer,
                            request=request.args
                                )
    else:
        print request.query_string
        return ('NO Location \n', 'recieved {}'.format(request.query_string))
