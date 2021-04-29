from flask import Flask,flash, redirect, url_for
from flask_migrate import Migrate
import os
from flask_login import logout_user
from app.user.admin import admin
from flask_user import SQLAlchemyAdapter, UserManager,login_required
from app.models import db
from app.models.user import UserModel
from app.models.store import StoreModel
basedir = os.path.abspath(os.path.dirname(__file__))

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    from app import models
    app.config['SECRET_KEY'] = "MYSecretKey236jkb56jk3b56bg54hg45y45h45"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "data.sqlite")

    app.config.from_object('app.settings')
    db.init_app(app)
    migrate.init_app(app, db,render_as_batch=True)
    db_adapter = SQLAlchemyAdapter(db, UserModel)  # Setup the SQLAlchemy DB Adapter
    UserManager(db_adapter, app)  # Init Flask-User and bind to app
    from app.user.views import user_blueprint
    from app.store.views import store_blueprint
    from app.main.views import main_blueprint
    from app.error_pages.handler import error_pages
    app.register_blueprint(error_pages)

    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(main_blueprint, url_prefix='/about')
    app.register_blueprint(user_blueprint, url_prefix="/UserModel")
    app.register_blueprint(store_blueprint, url_prefix="/StoreModel")

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash("მომხმარებელი გამოვიდა სისტემიდან")
        return redirect(url_for('main.home_page'))

    admin.init_app(app)
    return app

