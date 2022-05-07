from flask import render_template
from flask_login import login_required
from . import main

@main.route('/')
def index():
  '''function that renders the homepage'''
  title = 'Mistari'
  
  return render_template('index.html', title=title)

@main.route('/add')
@login_required
def add():
  '''function that renders the add page'''
  title = 'Mistari | Add a Pitch'
  
  return render_template('add.html', title=title)