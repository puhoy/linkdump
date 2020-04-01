from flask import request
from flask_security import http_auth_required, current_user

from linkdump import app
from linkdump.util.add_item import create_item


@app.route('/api/items', methods=['POST'])
@http_auth_required
def add_item():
    if current_user.is_anonymous:
        return '', 403
    url = request.json['url']
    html = request.json.get('html', None)

    success, item = create_item(current_user, url, html)
    if success:
        return 'added %s' % url, 200
    else:
        return 'couldnt add url', 500
