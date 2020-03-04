from readmelater.cli import cli


@cli.group('user')
def user_group():
    pass


from readmelater.cli.commands.user import add
from readmelater.cli.commands.user import get_items
from readmelater.cli.commands.user import list
from readmelater.cli.commands.user import flush_items
