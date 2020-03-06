import requests
from flask import request
from flask_security import http_auth_required, current_user

from linkdump import app, db
from linkdump.models import Item


@app.route('/items', methods=['POST'])
@http_auth_required
def add_item():
    if current_user.is_anonymous:
        return '', 403

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
    if item not in current_user.items.all():
        current_user.add_item(item)
    else:
        print('user already has this item')
    db.session.commit()
    return 'added %s' % url, 200