from unifi.controller import Controller
from unifi.controllerv2 import ControllerV2


def ControllerV(host, username, password, port, version, site_id='default'):
        if (version == 'v2'):
            return ControllerV2(host, username, password, port, version)
        else:
            return Controller(host, username, password, port, version, site_id)
