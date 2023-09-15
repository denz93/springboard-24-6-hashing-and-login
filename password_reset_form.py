from wtforms import Form, StringField, PasswordField
from wtforms.validators import InputRequired, Length, DataRequired

from register_form import MatchingWith

class PasswordResetForm(Form):
  code = StringField(
    id="code",
    name="code",
    label="Code",
    validators=[InputRequired(), DataRequired(), Length(min=6, max=6)]
  )
  new_password = PasswordField(
    id="new_password",
    name="new_password",
    label="New password",
    validators=[InputRequired(), DataRequired(), Length(min=6, max=32)]
  )
  repeate_new_password = PasswordField(
    id="repeate_new_password",
    name="repeate_new_password",
    label="Repeate new password",
    validators=[InputRequired(), DataRequired(), MatchingWith("new_password")]
  )