#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

from terUNIFI import create_app, db
from flask.ext.script import Manager, prompt_bool
from flask.ext.migrate import Migrate, MigrateCommand
from terUNIFI.models import WifiCtrl, WifiAp, Location, WifiType, \
    Company, Admixer
from terUNIFI.unifi_control import ControllerV
from admixer_locations import admixer_loc

app = create_app(os.getenv('TERUNIFI_ENV') or 'dev')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def upd_admixer():
    print '!!!!!!!!!!!!!!! --- Updating Admixer codes from file'
    for ad_loc in admixer_loc:
        db_loc = Location.get_by_name(ad_loc['location'])
        db_admixer = Admixer.get_by_loc_name(ad_loc['location'])
        if (db_admixer is None):
            print 'Found NEW Location Admixer ID:', ad_loc['location']
            ad_admixer = Admixer(
                    name=ad_loc['name'],
                    loc_name = ad_loc['location'],
                    ad_id=ad_loc['id'],
                    z_id=ad_loc['z'],
                 )
            db.session.add(ad_admixer)
    db.session.commit()
    for loc in Location.query.all():
        admixer_codes = Admixer.get_by_loc_name(loc.name)
        if admixer_codes:
            loc.admixer_id = admixer_codes.id
            db.session.commit()
            print '!!!! ----INDEXES--- ADDED or UPDATED'
        else:
            print '!!!!!!!! ---- Found Missing Admixer Location:',\
                loc.name

@manager.command
def upd_aps():
    print '!!!!!!!!!!!!!!! --- Cheking for AP changes'
# Adding New Locations if there were changes in AP names or new APs
    company = Company.query.get(1)
    for ctrl in company.wifictrls:
        c = ctrl.connect()
        for ap in c.get_aps():
            loc = ap['name'].split()[0]
            loc_ap = WifiAp.query.filter_by(ap_mac=ap['mac']).first()
            if (Location.query.filter_by(name=loc).first() == None):
                endp = ap['name'].split()[0].lower()
                add_location = Location(
                    name=loc,
                    endpoint=endp,
                    wifictrl_id=ctrl.id
                                        )
                db.session.add(add_location)
                db.session.commit()
                print '!!!!!!!!!!!!!!! --- Added Location: ', loc
# Adding New APs
            if (loc_ap is None):
                add_ap = WifiAp(
                        name=ap['name'],
                        ap_mac=ap['mac'],
                        usite="default",
                        wifictrl_id=ctrl.id,
                        location_id=Location.query.filter_by(
                                                        name=loc
                                                       ).first().id
                                 )
                db.session.add(add_ap)
                db.session.commit()
                print '!!!!!!!!!!!!!!! ---  Added AP: ', ap['name']
# Checking for Changes in AP name and assigning new Location
            elif (loc_ap.name != ap['name']):
                loc_ap.name = ap['name']
                loc_ap.wifictrl_id = ctrl.id
                loc_ap.location_id = Location.query.filter_by(
                                                        name=loc
                                                       ).first().id
                db.session.commit()
                print '!!!!!!!!!!!!!!! ---  Updated AP or Location: ',\
                    loc_ap.name


@manager.command
def restart_all_aps():
    print 'Restarting all APs'
    company = Company.query.get(1)
    for ctrl in company.wifictrls:
        c = ctrl.connect()
        for ap in c.get_aps():
            c.restart_ap(ap['mac'])

@manager.command
def initdb():
    db.create_all()
    print '!!!!!!!!!  ------  Initialized the DB '

# Creating free.lviv.ua Controller data

    add_company = Company(
                    name="PozitiFF",
                    description="PozitiFF LTD"
                          )
    add_wifi_type1 = WifiType(
                    made_by="UBNT",
                    firmware=2.0
                             )
    add_wifi_type2 = WifiType(
                    made_by="UBNT",
                    firmware=3.0
                             )
    add_wifi_ctrl1 = WifiCtrl(
                    name="unifi.nton.info",
                    description="UNIFI2",
                    url="unifi.nton.info",
                    usr="admin",
                    pwd="di3uvi",
                    port="8443",
                    endpoint="unifi2",
                    ver="V2",
                    type_id=1,
                    company_id=1
                              )
    add_wifi_ctrl2 = WifiCtrl(
                    name="unifi.nton.info",
                    description="UNIFI3",
                    url="unifi3.nton.info",
                    usr="admin",
                    pwd="di3uvi",
                    port="8443",
                    endpoint="unifi3",
                    ver="V3",
                    type_id=2,
                    company_id=1
                              )
    add_default_location1 = Location(
                    name='default',
                    endpoint='default',
                    wifictrl_id=1
                                 )
    add_default_location2 = Location(
                    name='default',
                    endpoint='default',
                    wifictrl_id=2
                                 )

    db.session.add(add_default_location1)
    db.session.add(add_default_location2)
    db.session.add(add_company)
    db.session.add(add_wifi_type1)
    db.session.add(add_wifi_type2)
    db.session.add(add_wifi_ctrl1)
    db.session.add(add_wifi_ctrl2)
    db.session.commit()
    print '!!!!!!!!!  ------  Company , Type and controllers added '
# Adding Locations
    company = Company.query.get(1)
    for ctrl in company.wifictrls:
        c = ctrl.connect()
        for ap in c.get_aps():
            loc = ap['name'].split()[0]
            if (Location.query.filter_by(name=loc).first() == None):
                endp = ap['name'].split()[0].lower()
                add_location = Location(
                    name=loc,
                    endpoint=endp,
                    wifictrl_id=ctrl.id
                                        )
                db.session.add(add_location)
                db.session.commit()
                print '!!!!!!!!!!!!!!! --- Added Location: ', loc
# Adding APs
            add_ap = WifiAp(
                    name=ap['name'],
                    ap_mac=ap['mac'],
                    usite="default",
                    wifictrl_id=ctrl.id,
                    location_id=Location.query.filter_by(name=loc).first().id
                    )
            db.session.add(add_ap)
            db.session.commit()
            print '!!!!!!!!!!!!!!! ---  Added AP: ', ap['name']


@manager.command
def dropdb():
    if prompt_bool("Are you sure"):
        db.drop_all()
        print 'Dropped the DB'


if __name__ == '__main__':
    manager.run()
