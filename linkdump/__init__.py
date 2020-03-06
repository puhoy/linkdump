import flask
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore

import logging
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_dramatiq import Dramatiq
from flask_misaka import Misaka

from linkdump.routes.forms.security.extended_register_form import ExtendedRegisterForm
# fix migration for sqlite: https://github.com/miguelgrinberg/Flask-Migrate/issues/61#issuecomment-208131722

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

migrate = Migrate()
logger = logging.getLogger(__name__)
dramatiq = Dramatiq()
misaka = Misaka()
# Setup Flask-Security

security = Security()
mail = Mail()

from linkdump.models import User, Role

def create_app():
    app = Flask(__name__,
                #static_url_path='/_static',
                template_folder='routes/frontend/templates')

    app.config.from_object('linkdump.config.default.DefaultConfig')
    app.config.from_envvar('LINKDUMP_SETTINGS')

    db.init_app(app)

    dramatiq.init_app(app)

    misaka.init_app(app)

    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role), register_form=ExtendedRegisterForm)

    mail.init_app(app)

    migration_dir = os.path.join(os.path.dirname(__file__), 'migrations')

    # fix migration for sqlite: https://github.com/miguelgrinberg/Flask-Migrate/issues/61#issuecomment-208131722
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True, directory=migration_dir, compare_type=True,
                             compare_server_default=True)
        else:
            migrate.init_app(app, db, directory=migration_dir, compare_type=True, compare_server_default=True)

        def url_for_self(**args):
            return flask.url_for(flask.request.endpoint, **{**flask.request.view_args, **flask.request.args, **args})

        app.jinja_env.globals['url_for_self'] = url_for_self

    @app.after_request
    def add_gnu_tp_header(response):
        # www.gnuterrypratchett.com
        response.headers.add("X-Clacks-Overhead", "GNU Terry Pratchett")
        return response

    return app


app = create_app()

from linkdump.routes.feeds import *
from linkdump.routes.api import *
from linkdump.routes.frontend import *

