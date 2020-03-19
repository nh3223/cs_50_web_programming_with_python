import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this_is_the_secret_key'
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
