from readmelater.cli import cli


@cli.group('item')
def item_group():
    pass


from readmelater.cli.commands.item import add