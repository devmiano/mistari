from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required, current_user

from app.main.forms import UpdateProfile, PitchForm
from ..models import User
from .. import db,photos
from . import main

@main.route('/')
def index():
  '''function that renders the homepage'''
  title = 'Challenge yourself with one of a kind pitch deck '
  
  return render_template('index.html', title=title)

@main.route('/user/<uname>')
def profile(uname):
  user = User.query.filter_by(username=uname).first()
  
  if user is None:
    abort(404)
    
  return render_template('profile/profile.html', user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
  user = User.query.filter_by(username=uname).first()
  
  if user is None:
    abort(404)
    
  update = UpdateProfile()
  
  if update.validate_on_submit():
    user.first_name = update.first_name.data
    user.last_name = update.last_name.data
    user.bio = update.bio.data
    
    
    db.session.add(user)
    db.session.commit()
    
    return redirect(url_for('.profile', uname=user.username))
    
  return render_template('profile/update.html', update=update)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
  user = User.query.filter_by(username=uname).first()
  if 'photo' in request.files:
    filename = photos.save(request.files['photo'])
    path = f'photos/{filename}'
    user.profile_pic_path = path
    db.session.commit()
    
  return redirect(url_for('main.profile', uname=uname))

@main.route('/add')
@login_required
def add():
  '''function that renders the add page'''
  title = 'Add a Pitch'
  
  return render_template('add.html', title=title)

@main.route('/add/new/<int:id>', methods=[ 'GET','POST'])
@login_required
def add_pitch(id):
  '''function that renders the add page'''
  title = 'Add a Pitch'
  pitch = PitchForm()
  
  
  return render_template('add.html', title=title)