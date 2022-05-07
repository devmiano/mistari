from flask import Flask
from flask_assets import Environment, Bundle
from config import config_options
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
  '''function to create and configure the Flask app'''
  app = Flask(__name__, static_folder='assets')
  app.config.from_object(config_options[config_name])
  db.init_app(app)
  assets = Environment(app)
  assets.url = app.static_url_path
  sass = Bundle('sass/global.scss', filters='pyscss', depends='sass/base/*.scss', output='styles/global.css')
  assets.config['PYSCSS_LOAD_PATHS'] = assets.load_path
  assets.config['PYSCSS_STATIC_URL'] = assets.url
  assets.config['PYSCSS_STATIC_ROOT'] = assets.directory
  assets.config['PYSCSS_ASSETS_URL'] = assets.url
  assets.config['PYSCSS_ASSETS_ROOT'] = assets.directory
  assets.register('sass_all', sass)
  sass.build()
  
  '''import and register the main blueprint'''
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)
  
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint, url_prefix='/auth')
  
  '''import and configure the requests for use in the app'''
  from .requests import configure_request
  configure_request(app)
  
  
  return app
