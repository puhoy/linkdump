from flask import render_template, flash, redirect, request
from flask_login import current_user
from sqlalchemy import func

from linkdump import app, db
from linkdump.models import Item, User
from linkdump.routes.forms.add_item import AddItemForm
from linkdump.routes.forms.feed_public import FeedPublicForm
from linkdump.util.add_item import create_item


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    users_with_public_feed = User.query.filter_by(feed_is_public=True).order_by(func.random()).limit(20)
    if current_user.is_anonymous:
        return render_template('index_anonymous.html.jinja2',
                               users_with_public_feed=users_with_public_feed)

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    add_item_form = AddItemForm()
    if add_item_form.add_item_submit.data and add_item_form.validate_on_submit():
        flash('item created')
        create_item(current_user, add_item_form.url.data)

    feed_public_form = FeedPublicForm()
    if feed_public_form.feed_public_submit.data and feed_public_form.validate_on_submit():
        flash('saved!')
        current_user.feed_is_public = feed_public_form.is_public.data == 'True'
        db.session.add(current_user)
        db.session.commit()

    if not current_user.feed_is_public:
        feed_public_form.feed_public_submit.label.text = 'make my feed public!'
        feed_public_form.is_public.data = True
    else:
        feed_public_form.feed_public_submit.label.text = 'DONT make my feed public!'
        feed_public_form.is_public.data = False
    
    items_pagination = current_user.items.order_by(Item.date_added.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('index.html.jinja2',
                           items_pagination=items_pagination,
                           users_with_public_feed=users_with_public_feed,
                           add_item_form=add_item_form,
                           feed_public_form=feed_public_form,
                           args=request.args)
