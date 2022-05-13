from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user
from datetime import datetime
from . import db
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


class User(UserMixin, db.Model):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(255))
  last_name = db.Column(db.String(255))
  username = db.Column(db.String(255), unique=True, index=True)
  email = db.Column(db.String(255), unique=True, index=True)
  bio = db.Column(db.String(255))
  profile_pic_path = db.Column(db.String(255))
  password_hash = db.Column(db.String(255))
  pitches = db.relationship('Pitch', backref='user', lazy='dynamic')
  comments = db.relationship('Comment', backref='user', lazy='dynamic')
  upvotes = db.relationship('Upvote', backref = 'user', lazy = 'dynamic')
  downvotes = db.relationship('Downvote', backref = 'user', lazy = 'dynamic')
  
  @property
  def password(self):
    raise AttributeError('you cannot read the password')
  
  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)
    
  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  def __repr__(self):
      return f'User {self.username}'

  
class Pitch(db.Model):
  __tablename__ = 'pitches'
  id = db.Column(db.Integer, primary_key=True)
  caption = db.Column(db.String(255), index = True)
  posted = db.Column(db.DateTime)
  author_id = db.Column(db.Integer,db.ForeignKey("users.id"), nullable = False)
  category = db.Column(db.String(255), nullable=False)
  comments = db.relationship('Comment', backref='pitch', lazy='dynamic')
  upvotes = db.relationship('Upvote', backref = 'pitch', lazy = 'dynamic')
  downvotes = db.relationship('Downvote', backref = 'pitch', lazy = 'dynamic')
  
  def save_pitch(self):
    db.session.add(self)
    db.session.commit()
  
  @classmethod
  def get_pitches(cls, id):
    pitches = Pitch.query.order_by(pitch_id=id).desc().all()
    return pitches
    
  
  def __repr__(self):
    return f'Pitch {self.caption}'
  
class Category(db.Model):
  __tablename__ = 'categories'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), unique=True, index=True)
  title = db.Column(db.String(255))
  
  def __repr__(self):
    return f'{self.name}'
  

class Comment(db.Model):
  __tablename__ = 'comments'
  id = db.Column(db.Integer, primary_key=True)
  caption = db.Column(db.String(255))
  author_id = db.Column(db.Integer ,db.ForeignKey("users.id"), nullable=False)
  pitch_id = db.Column(db.Integer, db.ForeignKey("pitches.id"), nullable= False)
  posted = db.Column(db.DateTime,default=datetime.utcnow)
  
  def save_comment(self):
    db.session.add(self)
    db.session.commit()
  
  def __repr__(self):
    return f'{self.caption}'
  
class Upvote(db.Model):
  __tablename__ = 'upvotes'
  id = db.Column(db.Integer,primary_key=True)
  upvote = db.Column(db.Integer,default=1)
  pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
  author_id = db.Column(db.Integer,db.ForeignKey('users.id'))

  def save_upvotes(self):
    db.session.add(self)
    db.session.commit()


  def add_upvotes(cls,id):
    upvote_pitch = Upvote(user = current_user, pitch_id=id)
    upvote_pitch.save_upvotes()

    
  @classmethod
  def get_upvotes(cls,id):
    upvote = Upvote.query.filter_by(pitch_id=id).all()
    return upvote

  @classmethod
  def get_all_upvotes(cls,pitch_id):
    upvotes = Upvote.query.order_by('id').all()
    return upvotes

  def __repr__(self):
    return f'{self.author_id}:{self.pitch_id}'



class Downvote(db.Model):
  __tablename__ = 'downvotes'

  id = db.Column(db.Integer,primary_key=True)
  downvote = db.Column(db.Integer,default=1)
  pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
  author_id = db.Column(db.Integer,db.ForeignKey('users.id'))

  def save_downvotes(self):
    db.session.add(self)
    db.session.commit()


  def add_downvotes(cls,id):
    downvote_pitch = Downvote(user = current_user, pitch_id=id)
    downvote_pitch.save_downvotes()

    
  @classmethod
  def get_downvotes(cls,id):
    downvote = Downvote.query.filter_by(pitch_id=id).all()
    return downvote

  @classmethod
  def get_all_downvotes(cls,pitch_id):
    downvote = Downvote.query.order_by('id').all()
    return downvote

  def __repr__(self):
    return f'{self.author_id}:{self.pitch_id}'