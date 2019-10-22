"""Flask config class."""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Set Flask configuration vars from .env file."""
    # General
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TESTING = os.environ.get('TESTING') or False
    DEBUG = os.environ.get('DEBUG') or False

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'book_wishlists.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False
    SQLALCHEMY_ECHO = False


class Development_Config(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class Testing_Config(Config):
    TESTING = True
