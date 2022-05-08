from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError,BooleanField,TextAreaField
from wtforms.validators import InputRequired,Email,EqualTo,Length

class UpdateProfile(FlaskForm):
  bio = TextAreaField('Tell us about you.',validators = [InputRequired()])
  submit = SubmitField('Submit')