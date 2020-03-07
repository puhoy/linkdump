from flask import render_template
from flask_login import current_user

from linkdump import app
from linkdump.models import Item


@app.route('/items/<int:item_id>', methods=['GET', 'POST'])
def item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return '', 404
    if not item in current_user.items:
        return '', 404
    return render_template('item.html', item=item)
