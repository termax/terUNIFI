from terUNIFI import app, db
from models import User, Company, WifiType, Location, WifiCtrl, WifiAp
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


admin.add_view(MyView(name='Hello'))
admin.register(Company, CompanyModel)
admin.register(User, UserModel)
