import requests
from flask import request
from flask_security import http_auth_required, current_user

from linkdump import app, db
from linkdump.models import Item
from linkdump.util.add_item import create_item


@app.route('/api/items', methods=['POST'])
@http_auth_required
def add_item():
    if current_user.is_anonymous:
        return '', 403
    url = request.json['url']
    success, item = create_item(current_user, url)
    if success:
        return 'added %s' % url, 200
    else:
        return 'couldnt add url', 500
