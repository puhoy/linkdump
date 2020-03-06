from flask import render_template

from linkdump import app


@app.route('/')
def index():
    return render_template('index.md')
