from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app.models.user import UserModel, Role, OAuth
from app.models import db
from flask import redirect, url_for, request, flash
from flask_user import current_user
from app.models.store import StoreModel
from flask_admin.menu import MenuLink


class UserModelView(ModelView):
    column_exclude_list = ['password', ]

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('UserModel.login', next=url_for("admin.index")))


class AdminModelView(ModelView):
    column_exclude_list = ['password', ]

    def is_accessible(self):
        # if current_user.is_authenticated:
        #     for emails in UserModel.email:
        #         if current_user in emails:
        return current_user.has_roles("Admin")

    def inaccessible_callback(self, name, **kwargs):
        flash('please authorize to verify that you have <Admin> status')
        return redirect(url_for('UserModel.login', next=url_for("admin.index")))


class IndexView(AdminIndexView):
    column_exclude_list = ['password', ]

    def is_accessible(self):
        print(current_user.email)
        return current_user.has_role("Admin")

    def inaccessible_callback(self, name, **kwargs):
        flash('please authorize to verify that you have <Admin> status')
        return redirect(url_for('UserModel.login', next=url_for("admin.index")))


admin = Admin(name='Panel', template_mode='bootstrap4', index_view=IndexView(name='home'))
admin.add_view(UserModelView(StoreModel, db.session))
admin.add_view(AdminModelView(UserModel, db.session, category="User Managements"))
admin.add_view(AdminModelView(OAuth, db.session, category="Oauth users"))
admin.add_view(UserModelView(Role, db.session, name="User Roles", category="User Managements"))
admin.add_link(MenuLink(name="Logout", endpoint='user.logout'))
