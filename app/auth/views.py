from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user,logout_user, login_required
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db
from . import auth
from ..email import mail_message

@auth.route('/login', methods=['GET', 'POST'])
def login():
  login = LoginForm()
  if login.validate_on_submit():
    user = User.query.filter_by(username = login.username.data).first()
    if user is not None and user.verify_password(login.password.data):
      login_user(user, login.remember.data)
      return redirect(request.args.get('next') or url_for('main.index'))
    
    flash('Invalid email or password')
  
  title = 'Sign in to your Account'
  return render_template('auth/login.html', title=title, login=login)

@auth.route('/signup', methods=['GET','POST'])
def signup():
  signup = RegistrationForm()
  if signup.validate_on_submit():
    user = User(username=signup.username.data, email=signup.email.data, password=signup.password.data)
    db.session.add(user)
    db.session.commit()
    
    mail_message('Welcome to Mistari', 'email/welcome_user', user.email, user=user)
    return redirect(url_for('auth.login'))
  
  title = 'Create a new Account'
  return render_template('auth/signup.html', signup=signup, title=title)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))