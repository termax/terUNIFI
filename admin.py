from terUNIFI import app, db
from models import User, Company, WifiType, Location, WifiCtrl, WifiAp, Event
from flask.ext.superadmin import Admin, BaseView, expose, model


# Create admin
admin = Admin(app, 'Simple Models')


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin-hello.html')


class CompanyModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'name')


class UserModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'username', 'email', 'company_id')


class WifiTypeModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'made_by', 'firmware', 'wifictrls')


class LocationModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'name', 'endpoint', 'description', 'admixer_id',
                    'wifictrl_id', 'wifi_aps')


class WifiCtrlModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'name', 'description', 'url', 'url', 'usr', 'pwd',
                    'endpoint', 'locations', 'wifi_aps', 'type_id',
                    'company_id')


class WifiApModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'name', 'ap_mac', 'usite', 'wifi_ctrl_id',
                    'location_id', 'events')


class EventModel(model.ModelAdmin):
    session = db.session
    list_display = ('id', 'date', 'ap_id', 'wifictrls')


admin.add_view(MyView(name='Hello'))
admin.register(Company, CompanyModel)
admin.register(User, UserModel)
admin.register(WifiType, WifiTypeModel)
admin.register(Location, LocationModel)
admin.register(WifiCtrl, WifiCtrlModel)
admin.register(WifiAp, WifiApModel)
admin.register(Event, EventModel)
