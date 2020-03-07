from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL


class AddItemForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Add')


