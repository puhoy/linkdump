from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField


class FeedPublicForm(FlaskForm):
    is_public = BooleanField('make my feed public', validators=[])
    feed_public_submit = SubmitField('save')


