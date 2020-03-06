from flask_security import ConfirmRegisterForm
from flask_security.forms import Required
from wtforms import StringField

from linkdump.routes.forms.security.util import unique_username


class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
    username = StringField('User Name', validators=[Required(), unique_username])
    pass
