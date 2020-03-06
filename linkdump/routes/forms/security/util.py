from flask_security import ConfirmRegisterForm
from flask_security.forms import Required
from wtforms import StringField, ValidationError
from linkdump import security


def unique_username(form, field):
    if security.datastore.get_user(field.data) is not None:
        msg = 'Username already taken.'
        raise ValidationError(msg)
