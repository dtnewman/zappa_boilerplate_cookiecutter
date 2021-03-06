# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

from {{ cookiecutter.app_name }}.settings import Local
from {{ cookiecutter.app_name }}.extensions import (
    db,
    login_manager,
    migrate,
)
from {{ cookiecutter.app_name }}.database import Base, init_engine
from {{ cookiecutter.app_name }}.assets import assets
from {{ cookiecutter.app_name }} import public, user

def create_app(config_object=Local):
    """
    An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    init_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    assets.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, Base)
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None

