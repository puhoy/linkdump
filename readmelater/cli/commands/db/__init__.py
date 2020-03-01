import click
from readmelater.cli import cli

@cli.group('db')
def db_group():
    pass

from readmelater.cli.commands.db.init import db_init
from readmelater.cli.commands.db.migrate import db_migrate
from readmelater.cli.commands.db.upgrade import db_upgrade

