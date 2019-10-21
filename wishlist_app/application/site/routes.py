from flask import Blueprint, render_template
from ..models import db, Wishlist, User, Book, Author

# Set up a Blueprint
mod = Blueprint('site', __name__,
                template_folder='templates',
                static_folder='static')


@mod.route('/')
@mod.route('/index')
def index():
    # users = db.session.query(User).all()
    users = db.session.query(User.first_name, User.last_name, User.email).all()
    books = db.session.query(Book).all()
    for b in books:
        print(b.author_id)
    # for u in users:
    #     print(u.first_name)
    # print(books)
    return render_template('site_index.html', users=users)
