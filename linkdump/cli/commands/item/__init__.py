from linkdump.cli import cli


@cli.group('item')
def item_group():
    pass


from linkdump.cli.commands.item.add import add_item
from linkdump.cli.commands.item.reprocess_all import reprocess_all
