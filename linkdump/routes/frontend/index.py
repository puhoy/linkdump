from flask import render_template, flash, redirect, request
from flask_login import current_user

from linkdump import app
from linkdump.models import Item
from linkdump.routes.forms.add_item import AddItemForm
from linkdump.util.add_item import create_item


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    add_item_form = AddItemForm()
    if add_item_form.validate_on_submit():
        flash('item created')
        create_item(current_user, add_item_form.url.data)

    pagination = current_user.items.order_by(Item.date_processing_started.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('index.html',
                           pagination=pagination,
                           add_item_form=add_item_form,
                           per_page=20, page=1)
