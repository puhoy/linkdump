from flask.cli import AppGroup


cli = AppGroup('cli')

from linkdump.cli.commands.item import item_group

