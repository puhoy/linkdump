from flask import render_template
from flask_login import current_user

from linkdump import app
from linkdump.models import Item


@app.route('/api', methods=['GET', 'POST'])
def api():
    return render_template('api.html.jinja2')
