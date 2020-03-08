from flask import render_template, request
from flask_login import login_required, current_user

from linkdump import app
from linkdump.models import Item
from linkdump.routes.forms.search import SearchForm


@login_required
@app.route('/search', methods=['GET', 'POST'])
def search():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    items_pagination = None
    query_string = ''

    search_form = SearchForm()
    if search_form.submit.data and search_form.validate_on_submit():
        query_string = search_form.query.data
        items = Item.search(search_form.query.data, user=current_user)
        items_pagination = items.order_by(Item.date_processing_started.desc()) \
            .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('search.html.jinja2',
                           search_form=search_form,
                           items_pagination=items_pagination,
                           query_string=query_string,
                           args=request.args)
