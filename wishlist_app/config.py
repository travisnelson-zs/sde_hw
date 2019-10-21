"""Flask config class."""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Set Flask configuration vars from .env file."""
    # General
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TESTING = os.environ.get('TESTING') or True
    DEBUG = os.environ.get('DEBUG') or True

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'book_wishlists.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False
    SQLALCHEMY_ECHO = True
