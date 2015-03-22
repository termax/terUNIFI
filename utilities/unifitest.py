from terUNIFI import app, db
from terUNIFI.models import WifiCtrl
from flask.ext.script import Command, Manager, Option, prompt_bool



manager = Manager(app)


@manager.option('-s', '--server', dest='server', default='unifi')
def connect(server):
    if (server == 'unifi'):
#        c = ControllerV('unifi.nton.info', 'admin', 'di3uvi', '8443', 'v2')
        c = WifiCtrl.connect_by_id(1)
    elif (server == 'unifi3'):
#        c = ControllerV('unifi3.nton.info', 'admin', 'di3uvi', '8443', 'v3')
        c = WifiCtrl.connect_by_id(2)
    else:
        print "No Such server"
        raise SystemExit

    all_aps = c.get_aps()
    ap_macs = dict([(ap['mac'], ap['ip']) for ap in all_aps])
    print ap_macs

@manager.command
def test():
    print "test"
    c = WifiCtrl.query.get(1).connect()


    #events = c.get_events()
    #print events
    #c.restart_ap_name('00:27:22:b2:fb:33')



    #c.restart_ap('00:27:22:b2:fb:33')

if __name__ == "__main__":
    manager.run()
