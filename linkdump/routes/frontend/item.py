from flask import render_template
from flask_login import current_user

from linkdump import app
from linkdump.models import Item

from lxml import etree


@app.route('/items/<int:item_id>', methods=['GET', 'POST'])
def item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return '', 404
    if not item in current_user.items:
        return '', 404
    body = etree.fromstring(item.body)
    while len(body) == 1:
        body = body[0]
    body.tag = 'section'
    item.body_as_section = etree.tostring(body).decode('utf-8')
    return render_template('item.html', item=item)
