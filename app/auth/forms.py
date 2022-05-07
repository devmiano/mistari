from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError,BooleanField
from wtforms.validators import InputRequired,Email,EqualTo,Length
from ..models import User

class RegistrationForm(FlaskForm):
  first_name = StringField('Enter your first name', validators=[InputRequired(), Length(min=4, max=100)])
  last_name = StringField('Enter your last name', validators=[InputRequired(), Length(min=4, max=100)])
  username = StringField('Enter your  username', validators=[InputRequired(), Length(min=4, max=100)])
  email = StringField('Enter your  email address', validators=[InputRequired(), Email()])
  password = PasswordField('Enter your password', validators=[InputRequired(), EqualTo('password_confirm', message='Passwords do not match'), Length(min=5)])
  password_confirm = PasswordField('Confirm your password', validators=[InputRequired()])
  submit = SubmitField('Sign up')
  
  def validate_username(self, data_field):
    if User.query.filter_by(username=data_field.data).first():
      raise ValidationError('That username is already taken')
    
  def validate_email(self, data_field):
    if User.query.filter_by(email=data_field.data).first():
      raise ValidationError('That email address is already in use')
    
class LoginForm(FlaskForm):
  email = StringField('Enter your  email address', validators=[InputRequired(), Email()])
  password = PasswordField('Enter your password', validators=[InputRequired()])
  remember = BooleanField('Remember me')
  submit = SubmitField('Log in')