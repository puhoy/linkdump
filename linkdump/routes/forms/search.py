from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    query = StringField('Search', validators=[])
    submit = SubmitField('search')


