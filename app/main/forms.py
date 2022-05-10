from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import InputRequired,Length

class UpdateProfile(FlaskForm):
  first_name = StringField('Enter your first name', validators=[InputRequired(), Length(min=4, max=100)])
  last_name = StringField('Enter your last name', validators=[InputRequired(), Length(min=4, max=100)])
  bio = TextAreaField('Tell us about you.',validators = [InputRequired()])
  submit = SubmitField('Submit')
  
class PitchForm(FlaskForm):
  caption = StringField('Enter your  caption')