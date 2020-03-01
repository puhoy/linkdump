import click
from flask.cli import FlaskGroup

from readmelater import create_app
from readmelater.get_content import UrlContent


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


from readmelater.cli.commands.db import db_group


@cli.command('add')
@click.argument('url')
def add(url):
    url_content = UrlContent(url)
    url_content.load()
    title = url_content.title
    doc = url_content.doc


@cli.command('add_user')
def add_user(user):
    pass

