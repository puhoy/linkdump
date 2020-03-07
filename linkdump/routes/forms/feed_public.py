from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField


class FeedPublicForm(FlaskForm):
    is_public = BooleanField('make my feed public', validators=[])
    submit = SubmitField('save')


