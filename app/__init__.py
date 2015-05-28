#encoding: utf-8
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache
from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
cache = Cache()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    cache.init_app(app)
    
    register_routes(app)
    
    return app

def register_routes(app):
    from .main import main as main_blueprint
    from .api_v1 import api_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app