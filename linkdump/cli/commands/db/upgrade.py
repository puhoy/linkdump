
from linkdump.cli.commands.db import db_group

from flask_migrate import init, migrate, upgrade


@db_group.command('upgrade')
def db_upgrade():
    upgrade()
