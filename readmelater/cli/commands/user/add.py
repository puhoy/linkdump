import click

from readmelater.cli.commands.user import user_group

from readmelater.models import User

@user_group.command('add')
@click.argument('name')
@click.argument('email')
def add_user(name, email):
    user = User.query.filter_by(email=email).first()
    if user:
        print('user already exists!')
        exit(0)
    user = User.create(name, email)
    click.echo('added %s' % user)

