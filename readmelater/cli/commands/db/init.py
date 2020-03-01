from readmelater.cli.commands.db import db_group
from readmelater import db

from flask_migrate import init, migrate, upgrade


@db_group.command('init')
def db_init():
    init()
