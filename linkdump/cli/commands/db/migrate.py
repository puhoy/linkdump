from linkdump.cli.commands.db import db_group

import click
from flask_migrate import init, migrate, upgrade


@db_group.command('migrate')
def db_migrate():
    migrate()
