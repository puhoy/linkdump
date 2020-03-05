from linkdump.cli import cli


@cli.group('user')
def user_group():
    pass


from linkdump.cli.commands.user import add
from linkdump.cli.commands.user import get_items
from linkdump.cli.commands.user import list
from linkdump.cli.commands.user import flush_items
