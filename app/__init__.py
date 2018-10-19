from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail

bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
db = SQLAlchemy()
mail =Mail()


def getApp(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    # 注册主页blueprint
    from .main import main as blueprint_main
    app.register_blueprint(blueprint_main)
    # 注册api blueprint
    from .api_1_0 import api as blueprint_api
    app.register_blueprint(blueprint_api, url_prefix='/homework/api/v1.0')
    return app
