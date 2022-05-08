import os

class Config:
  '''class to configure url parameters'''
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  UPLOADED_PHOTOS_DEST ='app/assets/photos'
  
class ProdConfig(Config):
  pass

class DevConfig(Config):
  SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://devmiano:devmiano@localhost/mistari"
  DEBUG = True
  ASSETS_DEBUG = True
  
config_options = {
  'development': DevConfig,
  'production': ProdConfig
}
  