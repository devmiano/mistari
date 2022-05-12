from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
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
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
  pitches = db.relationship('Pitch', backref='user', lazy='dynamic')
  comments = db.relationship('Comment', backref='user', lazy='dynamic')
  
  @property
  def password(self):
    raise AttributeError('you cannot read the password')
  
  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)
    
  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  @classmethod
  def get_user(cls, usr):
    usr_id = User.query.filter_by(username=usr).first()
    return usr_id
  
  def __repr__(self):
      return f'User {self.username}'
    
class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255))
  users = db.relationship('User', backref='role', lazy='dynamic')
  
  def __repr__(self):
    return f'Role {self.name}'
  
class Pitch(db.Model):
  __tablename__ = 'pitches'
  id = db.Column(db.Integer, primary_key=True)
  caption = db.Column(db.String(255))
  posted = db.Column(db.DateTime,default=datetime.utcnow)
  user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
  category = db.Column(db.String(255))
  comments = db.relationship('Comment', backref='pitch', lazy='dynamic')
  upvote = db.Column(db.Integer)
  downvote = db.Column(db.Integer)
  
  def save_pitch(self):
    db.session.add(self)
    db.session.commit()
    
  
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
  user_id = db.Column(db.Integer ,db.ForeignKey("users.id"))
  pitch_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))
  posted = db.Column(db.DateTime,default=datetime.utcnow)
  
  def save_comment(self):
    db.session.add(self)
    db.session.commit()
  
  
  @classmethod
  def get_pitch_comments(cls, pitch_id):
    pitch_comments = Comment.query.filter_by(pitch_id=pitch_id).all()
    return pitch_comments
  
  @classmethod
  def get_user_comments(cls, user_id):
    user_comments = Comment.query.filter_by(user_id=user_id).all()
    return user_comments
  
  def __repr__(self):
    return f'{self.comment}'