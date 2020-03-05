import click
import requests

from linkdump import db
from linkdump.cli.commands.item import item_group
from linkdump.models import User, Item


@item_group.command('add')
@click.argument('user_email')
@click.argument('url')
def add_item(user_email, url):
    user = User.query.filter_by(email=user_email).first()
    if not user:
        click.echo('user not found')
        exit(1)
    
    response = requests.head(url)
    if not response.ok:
        click.echo('failed to head %s: %s' % (url, response.text))
        exit(1)
    
    (created, item) = Item.create(source=url)
    item: Item
    if created:
        print('item %s created' % item)
        item.process()
    else:
        print('using item %s from db' % item)
    if item not in user.items.all():
        user.add_item(item)
    else:
        print('user already has this item')
    db.session.add(user)

    click.echo('processed item: %s' % item)
    click.echo('title: %s' % item.title)
    click.echo('body: %s' % item.body)

