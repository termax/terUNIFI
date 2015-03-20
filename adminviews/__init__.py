from .. import db
from flask.ext.superadmin import model


class CompanyModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'name')


class UserModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'username', 'email', 'company_id')


class WifiTypeModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'made_by', 'firmware')


class LocationModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'name', 'endpoint', 'description', 'admixer_id',
                    'wifictrl_id')


class WifiCtrlModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'name', 'description', 'url', 'url', 'usr', 'pwd',
                    'endpoint', 'type_id',
                    'company_id')


class WifiApModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'name', 'ap_mac', 'usite', 'wifi_ctrl_id',
                    'location_id')


class AdmixerModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'name', 'ad_id', 'z_id')


class EventModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'date', 'ap_id')


class DeviceModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'device_mac')
