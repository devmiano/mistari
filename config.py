import os

class Config:
  '''class to configure url parameters'''
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  UPLOADED_PHOTOS_DEST ='app/assets/photos'
  MAIL_SERVER = 'smtp.googlemail.com'
  MAIL_PORT = 587
  MAIL_USE_TLS = True
  MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
  MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
  
class ProdConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
  # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)


class DevConfig(Config):
  SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://devmiano:devmiano@localhost:5432/mistari"
  DEBUG = True
  ASSETS_DEBUG = True
  
config_options = {
  'development': DevConfig,
  'production': ProdConfig
}
  