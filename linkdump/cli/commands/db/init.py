from linkdump.cli.commands.db import db_group
from linkdump import db

from flask_migrate import init, migrate, upgrade


@db_group.command('init')
def db_init():
    init()
