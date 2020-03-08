import click

from linkdump.cli.commands.item import item_group
from linkdump.models import Item


@item_group.command('reprocess_all')
def reprocess_all():
    items = Item.query.all()
    for item in items:
        click.echo('processing %s' % item)
        item.process()
