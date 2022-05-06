from flask import render_template

from . import main

@main.route('/')
def index():
  '''function that renders the homepage and the headlines'''
  title = 'Mistari'
  
  return render_template('index.html', title=title)