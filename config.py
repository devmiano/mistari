import os

class Config:
  '''class to configure url parameters'''
  SECRET_KEY = os.environ.get('SECRET_KEY')
  
  
  
class ProdConfig(Config):
  pass

class DevConfig(Config):
  DEBUG = True
  ASSETS_DEBUG = True
  
config_options = {
  'development': DevConfig,
  'production': ProdConfig
}
  