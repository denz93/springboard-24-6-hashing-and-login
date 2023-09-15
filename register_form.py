from wtforms import Form, Field, ValidationError, StringField, PasswordField, EmailField
from wtforms.validators import Length, InputRequired, Email, DataRequired

def MatchingWith(target_field_name):
  def wrapper(form: Form, field: Field):
    target:Field = form._fields.get(target_field_name)
    if target.data != field.data:
      raise ValidationError(f"{field.name} does not match with {target_field_name}")
  return wrapper
  
class RegisterForm(Form):
  username = StringField(
    id="username", 
    label="Username", 
    validators=[Length(min=1, max=20), InputRequired(), DataRequired()])
  password = PasswordField(
    id="password",
    label="Password",
    validators=[Length(min=6, max=32), InputRequired(), DataRequired()]
  )
  repassword = PasswordField(
    id="repassword",
    label="Re-password",
    validators=[MatchingWith("password"), InputRequired(), DataRequired()]
  )

  email = EmailField(
    id="email",
    name="email",
    label="Email",
    validators=[Email(), InputRequired(), DataRequired()]
  )

  first_name = StringField(
    id="first_name",
    name="first_name",
    label="First name",
    validators=[DataRequired(), InputRequired(), Length(0, 30)]
  )
  last_name = StringField(
    id="last_name",
    name="last_name",
    label="Last name",
    validators=[DataRequired(), InputRequired(), Length(0, 30)]
  )