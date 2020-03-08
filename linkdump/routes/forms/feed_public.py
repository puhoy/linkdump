from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField


class FeedPublicForm(FlaskForm):
    is_public = HiddenField('is_public', validators=[])
    feed_public_submit = SubmitField('Make my feed public!')
