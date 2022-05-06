secret_key = None


def configure_request(app):
  '''function that configures the request object needed for running the application'''
  global secret_key
  secret_key = app.config['SECRET_KEY']