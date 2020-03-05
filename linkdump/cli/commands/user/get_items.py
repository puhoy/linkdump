from xml.etree import ElementTree

import click

from linkdump.cli.commands.user import user_group

from linkdump.models import Item, User


def remove_tags(text):
    return ''.join(ElementTree.fromstring(text).itertext())


@user_group.command('get_items')
@click.argument('email')
@click.option('--as-text', is_flag=True, default=True)
def get_items(email, as_text):
    user = User.query.filter_by(email=email).first()
    if not user:
        click.echo('could not find user')
        exit(1)
    click.echo('user has %s items' % len(user.items.all()))
    for item in user.items.all():
        item: Item
        click.secho(item.title, color='green', bold=True)
        click.secho('started @%s' % item.date_processing_started)
        click.secho('finished @%s' % item.date_processing_finished)


