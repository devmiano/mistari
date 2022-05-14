from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required, current_user
from datetime import datetime as dt

from app.main.forms import AddPitch, UpdateProfile, AddComment
from ..models import Pitch, User, Category, Downvote, Upvote, Comment
from .. import db,photos
from . import main

@main.route('/')
def index():
  '''function that renders the homepage'''
  title = 'Challenge yourself with one of a kind pitch deck '
  upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)
  pitch = Pitch.query.order_by(Pitch.posted.desc()).all()
 
  
  return render_template('index.html', title=title, upvotes=upvotes, pitch=pitch)

@main.route('/elevator')
def elevator():
  '''function that renders the homepage'''
  title = 'The Elevator Pitch'
  upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)
  elevator = Pitch.query.filter_by(category='elevator').order_by(Pitch.posted).all()
  
  return render_template('category/elevator.html', title=title, upvotes=upvotes, elevator=elevator)


@main.route('/word')
def word():
  '''function that renders the homepage'''
  title = 'The One Word Pitch'
  upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)
  word = Pitch.query.filter_by(category='word').order_by(Pitch.posted).all()
  
  return render_template('category/word.html', title=title, upvotes=upvotes, word=word)


@main.route('/competitor')
def competitor():
  '''function that renders the homepage'''
  title = 'The Competitor Pitch'
  upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)
  competitor = Pitch.query.filter_by(category='competitor').order_by(Pitch.posted).all()
  
  return render_template('category/competitor.html', title=title, upvotes=upvotes, competitor=competitor)


@main.route('/twitter')
def twitter():
  '''function that renders the homepage'''
  title = 'The Twitter Pitch'
  upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)
  twitter = Pitch.query.filter_by(category='twitter').order_by(Pitch.posted).all()
  
  return render_template('category/twitter.html', title=title, upvotes=upvotes, twitter=twitter)


@main.route('/question')
def question():
  '''function that renders the homepage'''
  title = 'The Question Pitch'
  upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)
  question = Pitch.query.filter_by(category='question').order_by(Pitch.posted).all()
  
  return render_template('category/question.html', title=title, upvotes=upvotes, question=question)


@main.route('/rhyme')
def rhyme():
  '''function that renders the homepage'''
  title = 'The Rhyme Pitch'
  upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)
  rhyme = Pitch.query.filter_by(category='rhyme').order_by(Pitch.posted).all()
  
  return render_template('category/rhyme.html', title=title, upvotes=upvotes, rhyme=rhyme)


@main.route('/pixar')
def pixar():
  '''function that renders the homepage'''
  title = 'The Pixar Pitch'
  upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)
  pixar = Pitch.query.filter_by(category='pixar').order_by(Pitch.posted).all()
  
  return render_template('category/pixar.html', title=title, upvotes=upvotes, pixar=pixar)


@main.route('/user/<uname>')
def profile(uname):
  
  user = User.query.filter_by(username=uname).first()
  author_id=current_user._get_current_object().id,
  pitch = Pitch.query.filter_by(id=author_id).order_by(Pitch.posted).all()
  
  if user is None:
    abort(404)
    
  title = f'{user.first_name} {user.last_name}'
    
  return render_template('profile/profile.html', user=user, pitch=pitch, title=title)


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
  
  title = f'{user.first_name} {user.last_name} Update Profile'
    
  return render_template('profile/update.html', update=update, title=title)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
  user = User.query.filter_by(username=uname).first()
  if 'photo' in request.files:
    filename = photos.save(request.files['photo'])
    path = f'photos/{filename}'
    user.profile_pic_path = path
    db.session.commit()
    
    title = f'{user.first_name} {user.last_name} Update Pic'
    
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
  now = dt.now()
  
  
  
  if cname == category.name and add_pitch.validate_on_submit():
    caption = add_pitch.caption.data
    author_id = current_user._get_current_object().id
    category = category.name
    posted = now.strftime("%a %d %b %Y %I:%M:%S")
    pitch = Pitch(caption=caption, author_id=author_id, category=category, posted=posted)
    
    db.session.add(pitch)
    db.session.commit()
    
    return redirect(url_for('main.index'))
  
  title = f'Add {category.title}'
  
  return render_template('profile/create.html', title=title, form=add_pitch, uname=user.username, cname=category.name)


@main.route('/comment/new/<int:pitch_id>', methods = ['GET','POST'])
@login_required
def comment(pitch_id):
  form = AddComment()
  pitch=Pitch.query.get(pitch_id)
  now = dt.now()
  if form.validate_on_submit():
    caption = form.caption.data
    posted = now.strftime("%a %d %b %Y %I:%M:%S")

    comment = Comment(caption=caption, author_id=current_user._get_current_object().id, pitch_id=pitch_id, posted=posted)
    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('main.comment', pitch_id= pitch_id))
  title = 'Comment'
  comments = Comment.query.filter_by(pitch_id=pitch_id).all()
  return render_template('comment.html', form=form, comments=comments, pitch=pitch, title=title )


@main.route('/pitch/upvote/<int:pitch_id>/new', methods = ['GET', 'POST'])
@login_required
def upvote(pitch_id):
  user = current_user
    
  if Upvote.query.filter(Upvote.author_id==user.id,Upvote.pitch_id==pitch_id).first():
    return  redirect(url_for('main.index'))


  new_upvote = Upvote(pitch_id=pitch_id, user=current_user)
  new_upvote.save_upvotes()
  return redirect(url_for('main.index'))


@main.route('/pitch/downvote/<int:pitch_id>/new', methods = ['GET', 'POST'])
@login_required
def downvote(pitch_id):
  user = current_user
    
  if Downvote.query.filter(Downvote.author_id==user.id,Downvote.pitch_id==pitch_id).first():
    return  redirect(url_for('main.index'))

  
  new_downvote = Downvote(pitch_id=pitch_id, user = current_user)
  new_downvote.save_downvotes()
  return redirect(url_for('main.index'))