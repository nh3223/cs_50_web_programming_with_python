import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this_is_the_secret_key'
    
    if not os.environ.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is not set")
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.getenv("DATABASE_URL")
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    

