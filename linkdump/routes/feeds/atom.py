import requests
from flask import request, url_for
from urllib.parse import urljoin

from flask_login import login_required

from linkdump import app, db
from linkdump.models import User, Item

from feedgen.feed import FeedGenerator
import pytz


def get_feed(user):
    fg = FeedGenerator()
    fg.id(urljoin(app.config['BASE_URL'], user.email))
    fg.title('%ss feed' % user.username)
    fg.author({'name': user.username, 'email': user.email})
    return fg


@app.route('/feeds/atom/<username>')
@login_required
def feed(username):
    format = request.args.get('format', 'html')

    user = User.query.filter_by(email=username).first()
    if not user:
        return ''

    feed = get_feed(user)
    for item in user.items:
        if item.date_processing_finished:
            entry = feed.add_entry()
            entry.id(url_for('feed_item', username=user.username, item_id=item.id))
            entry.title(item.title)
            if format == 'html':
                entry.content(item.body)
            elif format == 'text':
                entry.content(item.body_plain_text)
            entry.link(href=item.source)

            timestamp = pytz.utc.localize(item.date_processing_finished)
            entry.pubDate(timestamp)
            entry.updated(timestamp)

    atomfeed = feed.atom_str(pretty=True)
    return atomfeed


@app.route('/feeds/atom/<user_email>/<item_id>')
def feed_item(user_email, item_id):
    item = Item.query.get(item_id)
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return '', 404
    if user in item.users:
        return item.body
    return '', 404
