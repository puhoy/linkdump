import requests
from flask import request, url_for
from urllib.parse import urljoin
from readmelater import app, db
from readmelater.models import User, Item

from feedgen.feed import FeedGenerator
import pytz


def get_feed(user):
    fg = FeedGenerator()
    fg.id(urljoin(app.config['BASE_URL'], user.email))
    fg.title('%ss feed' % user.username)
    fg.author({'name': user.username, 'email': user.email})
    return fg


@app.route('/feeds/atom/<user_email>', methods=['GET', 'POST'])
def feed(user_email):
    if request.method == 'GET':
        format = request.args.get('format', 'html')

        user = User.query.filter_by(email=user_email).first()
        if not user:
            return ''

        feed = get_feed(user)
        for item in user.items:
            if item.date_processing_finished:
                entry = feed.add_entry()
                entry.id(url_for('feed_item', user_email=user.email, item_id=item.id))
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

    elif request.method == 'POST':
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return ''
        url = request.json['url']
        response = requests.head(url)
        if not response.ok:
            return 'cant access %s' % url

        (created, item) = Item.create(source=url, process=True)
        item: Item
        if created:
            print('item %s created' % item)
        else:
            print('using item %s from db' % item)
        if item not in user.items.all():
            user.add_item(item)
        else:
            print('user already has this item')
        db.session.commit()
        return 'added %s' % url, 200


@app.route('/feeds/atom/<user_email>/<item_id>')
def feed_item(user_email, item_id):
    item = Item.query.get(item_id)
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return '', 404
    if user in item.users:
        return item.body
    return '', 404
