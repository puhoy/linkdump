from urllib.parse import urljoin

import pytz
from feedgen.feed import FeedGenerator
from flask import request, url_for
from flask_security import http_auth_required, current_user

from linkdump import app
from linkdump.models import User, Item


def get_feed(user):
    fg = FeedGenerator()
    fg.id(urljoin(app.config['BASE_URL'], user.email))
    fg.title('%ss feed' % user.username)
    fg.author({'name': user.username, 'email': user.email})
    return fg



@app.route('/feeds/atom/')
@http_auth_required
def feed():
    if not current_user.is_anonymous:
        format = request.args.get('format', 'html')
        user = User.query.filter_by(email=current_user.email).first()
        if not user:
            return ''

        feed = get_feed(user)
        for item in user.items:
            if item.date_processing_finished:
                entry = feed.add_entry()
                entry.id(url_for('feed_item', item_id=item.id))
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


@app.route('/feeds/atom/<item_id>')
def feed_item(item_id):
    item = Item.query.get(item_id)
    if current_user in item.users:
        return item.body
    return '', 404
