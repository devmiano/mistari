from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required, current_user

from app.main.forms import AddPitch, UpdateProfile
from ..models import Pitch, User, Category
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

@main.route('/user/<uname>/add',methods=['GET', 'POST'])
@login_required
def add(uname):
  user = User.query.filter_by(username=uname).first()
  '''function that renders the add page'''
  title = 'Choose a Category'
  
  
  if user is None:
    abort(404)
  
  categories = Category.query.all()
  
  return render_template('profile/add.html', title=title, categories=categories, uname=user.username)

@main.route('/user/<uname>/add/<cname>',methods=['GET', 'POST'])
@login_required
def create(uname, cname):
  user = User.query.filter_by(username=uname).first()
  category = Category.query.filter_by(name=cname).first()
  add_pitch = AddPitch()
  '''function that renders the add page'''
  
  
  if cname == 'elevator' and add_pitch.validate_on_submit():
    caption = add_pitch.caption.data
    author_id = current_user._get_current_object().id
    category = category.name
    pitch = Pitch(caption=caption, author_id=author_id, category=category)
    
    db.session.add(pitch)
    db.session.commit()
    
    return redirect(url_for('main.index'))
  
  title = f'{category.title}'
  
  return render_template('profile/create.html', title=title, form=add_pitch, uname=user.username, cname=category.name)

