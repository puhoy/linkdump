import click
from linkdump.cli import cli
from linkdump.models import *

@cli.group('_db')
def db_group():
    pass


from linkdump.cli.commands.db.init import db_init
from linkdump.cli.commands.db.migrate import db_migrate
from linkdump.cli.commands.db.upgrade import db_upgrade

