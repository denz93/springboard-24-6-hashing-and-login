from wtforms import Form, StringField, EmailField, ValidationError
from wtforms.validators import InputRequired, DataRequired, Length, Email, StopValidation, email
def EitherExist(target_field_name):
  def wrapper(form, field):
    if (len(field.data) > 0 and len(form.data[target_field_name]) > 0)\
      or (len(field.data) == 0 and len(form.data[target_field_name]) == 0):
      raise StopValidation(f'should provide either "{target_field_name}" or "{field.name}"')
  return wrapper
def EmailIfExist():
  verify = Email()
  def wrapper(form, field):
    if len(field.data) > 0:
      verify(form, field)
  return wrapper

class PasswordResetCodeGenerateForm(Form):
  email = EmailField(
    id="email",
    name="email",
    label="Email",
    validators=[EitherExist('username'), EmailIfExist()]
  )
  username = StringField(
    id="username",
    name="username",
    label="Username",
    validators=[Length(max=20)]
  )