import click
from flask.cli import FlaskGroup

from readmelater import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


from readmelater.cli.commands.db import db_group
from readmelater.cli.commands.user import user_group
from readmelater.cli.commands.item import item_group

