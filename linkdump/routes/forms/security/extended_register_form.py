from flask_security.forms import RegisterForm, Required
from wtforms import StringField
from linkdump.routes.forms.security.util import unique_username

class ExtendedRegisterForm(RegisterForm):
    username = StringField('User Name', validators=[Required(), unique_username])


