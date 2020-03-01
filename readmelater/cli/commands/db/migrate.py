from readmelater.cli.commands.db import db_group

import click
from flask_migrate import init, migrate, upgrade


@db_group.command()
def db_migrate():
    migrate()
