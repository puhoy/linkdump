from linkdump.cli import cli


@cli.group('item')
def item_group():
    pass


from linkdump.cli.commands.item import add