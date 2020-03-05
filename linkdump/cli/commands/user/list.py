import click

from linkdump.cli.commands.user import user_group

from linkdump.models import User

@user_group.command('list')
def list():
    users = User.query.all()
    for user in users:
        click.echo('%s: %s' % (user, user.email))

