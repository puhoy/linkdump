from flask import request, url_for
from xml.etree import ElementTree
from urllib.parse import urljoin
from readmelater import app
from readmelater.models import User, Item

from feedgen.feed import FeedGenerator


def get_feed(user):
    fg = FeedGenerator()
    fg.id(urljoin(app.config['BASE_URL'], user.email))
    fg.title('%ss feed' % user.username)
    fg.author({'name': user.username, 'email': user.email})
    return fg


def remove_tags(text):
    return ''.join(ElementTree.fromstring(text).itertext())


@app.route('/feeds/atom/<user_email>')
def html_feed(user_email):
    format = request.args.get('format', 'html')

    user = User.query.filter_by(email=user_email).first()
    if not user:
        return ''

    feed = get_feed(user)
    for item in user.items:
        entry = feed.add_entry()
        entry.id(item.title)
        entry.title(item.title)
        if format == 'html':
            entry.content(item.body)
        elif format == 'text':
            entry.content(remove_tags(item.body))
        entry.link(href=url_for('item', user_email=user.email, item_id=item.id))

    atomfeed = feed.atom_str(pretty=True)
    return atomfeed

@app.route('/feeds/atom/<user_email>/<item_id>')
def item(user_email, item_id):
    item = Item.query.get(item_id)
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return ''
    if user in item.users:
        return item.body
    return ''

