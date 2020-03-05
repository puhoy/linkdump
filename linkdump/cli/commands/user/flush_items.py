import click

from linkdump import db
from linkdump.cli.commands.user import user_group
from linkdump.models import User


@user_group.command('flush_items')
@click.argument('email')
@click.option('--as-text', is_flag=True, default=True)
def flush_items(email, as_text):
    user = User.query.filter_by(email=email).first()
    if not user:
        click.echo('could not find user')
        exit(1)
    click.echo('user has %s items' % len(user.items.all()))
    for item in user.items.all():
        print('deleting %s' % item)
        db.session.delete(item)
    db.session.commit()
