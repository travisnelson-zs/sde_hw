from flask import Blueprint, render_template
from ..models import db, Wishlist, User, Book, Author

# Set up a Blueprint
mod = Blueprint('site', __name__,
                template_folder='templates',
                static_folder='site/static')


@mod.route('/')
@mod.route('/index')
def index():
    users = db.session.query(User).all()
    books = db.session.query(Book, Author).join(Author).all()
    return render_template('site_index.html', users=users, books=books)
