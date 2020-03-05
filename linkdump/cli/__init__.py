import click
from flask.cli import FlaskGroup

from linkdump import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


from linkdump.cli.commands.db import db_group
from linkdump.cli.commands.user import user_group
from linkdump.cli.commands.item import item_group

