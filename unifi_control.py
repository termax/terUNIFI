from unifi.controller import Controller
from unifi.controllerv2 import ControllerV2


def ControllerV(host, username, password, port, version, site_id='default'):
        if (version == 'V2' or version == 'v2'):
            return ControllerV2(host, username, password, port, version)
        elif (version == 'V3' or version == 'v2'):
            return Controller(host, username, password, port, version, site_id)
        else:
            return Controller(host, username, password, port, version, site_id)
