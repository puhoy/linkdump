from flask import render_template
from flask_login import current_user, login_required

from linkdump import app
from linkdump.models import Item

from lxml import etree
from itsdangerous.url_safe import URLSafeSerializer

serializer = URLSafeSerializer(app.config['SECRET_KEY'])


def render_item(item):
    body = etree.fromstring(item.body)
    while len(body) == 1:
        body = body[0]
    body.tag = 'section'
    item_key = serializer.dumps(item.id)
    item.body_as_section = etree.tostring(body).decode('utf-8')
    return render_template('item.html', item=item, item_key=item_key)


@login_required
@app.route('/items/<int:item_id>', methods=['GET', 'POST'])
def item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return '', 404
    if not item in current_user.items:
        return '', 404
    return render_item(item)


@app.route('/items/shared/<item_key>')
def item_shared(item_key):
    item_id = serializer.loads(item_key)
    item = Item.query.get(item_id)
    return render_item(item)
