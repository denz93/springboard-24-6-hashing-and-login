from wtforms import Form, Field, StringField, PasswordField
from wtforms.validators import Length, InputRequired

class LoginForm(Form):
  username = StringField(id="username",
                   name="username",
                   label="Username",
                   validators=[Length(min=1, max=20), InputRequired()]
                   )
  password = PasswordField(id="password",
                   label="Password",
                   name="password",
                   validators=[Length(min=1, max=32), InputRequired()])