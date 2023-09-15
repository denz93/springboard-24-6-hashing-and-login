from wtforms import Field, Form, StringField, TextAreaField
from wtforms.validators import InputRequired, Length, DataRequired
from wtforms.widgets import TextArea
class FeedbackFormCreate(Form):
  title = StringField(
    id="title",
    name="title",
    label="Title",
    validators=[Length(min=1, max=100), InputRequired(), DataRequired()]
  )

  content = TextAreaField(
    id="content",
    name="content",
    label="Content",
    validators=[Length(min=1, max=1000), InputRequired(), DataRequired()]
  )

class FeedbackFormUpdate(FeedbackFormCreate):
  pass