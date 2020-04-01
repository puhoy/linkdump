import flask
from flask_mail import Mail, Message
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import user_registered, user_confirmed

import logging
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_dramatiq import Dramatiq
from flask_misaka import Misaka

from flask_cors import CORS

logger = logging.getLogger(__name__)

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
misaka = Misaka()

security = Security()
dramatiq = Dramatiq()
mail = Mail()


def create_app():
    from linkdump.routes.forms.security.extended_register_form import ExtendedRegisterForm
    from linkdump.routes.forms.security.extended_confirm_register_form import ExtendedConfirmRegisterForm
    from linkdump.models import User, Role
    from linkdump.util.send_mail import _send_mail_task

    app = Flask(__name__,
                static_folder='routes/frontend/static',
                template_folder='routes/frontend/templates')

    app.config.from_object('linkdump.config.default.DefaultConfig')
    app.config.from_envvar('LINKDUMP_SETTINGS')

    CORS(app)

    db.init_app(app)
    dramatiq.init_app(app)
    misaka.init_app(app)
    security_ctx = security.init_app(app, SQLAlchemyUserDatastore(db, User, Role),
                                     register_form=ExtendedRegisterForm,
                                     confirm_register_form=ExtendedConfirmRegisterForm)
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

    @security_ctx.send_mail_task
    def security_send_mail(msg: Message):
        _send_mail_task.send(subject=msg.subject, sender=msg.sender,
                             recipients=msg.recipients, body=msg.body,
                             html=msg.html)

    @user_registered.connect_via(app)
    def user_registered_hook(*args, **kwargs):
        msg = dict(
            sender=app.config['SECURITY_EMAIL_SENDER'],
            subject='new registration on %s' % (app.config['SERVER_NAME']),
            recipients=[app.config['SECURITY_EMAIL_SENDER']],
            body='%s just registered on %s' % (kwargs['user'].email, app.config['SERVER_NAME'])
        )
        _send_mail_task.send(**msg)

    @user_confirmed.connect_via(app)
    def user_confirmed_hook(*args, **kwargs):
        msg = dict(
            sender=app.config['SECURITY_EMAIL_SENDER'],
            subject='new confirmation on %s' % (app.config['SERVER_NAME']),
            recipients=[app.config['SECURITY_EMAIL_SENDER']],
            body='%s just confirmed on %s' % (kwargs['user'].email, app.config['SERVER_NAME'])
        )
        _send_mail_task.send(**msg)

    return app


app = create_app()

from linkdump.cli import cli

app.cli.add_command(cli)

from linkdump.routes.feeds import *
from linkdump.routes.api import *
from linkdump.routes.frontend import *
