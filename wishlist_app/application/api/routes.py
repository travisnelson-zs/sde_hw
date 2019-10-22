from flask import Blueprint, jsonify, request
from ..models import db, Wishlist, User, Book, Author
from .errors import bad_request, invalid_get_target

# Set up a Blueprint
mod = Blueprint('api', __name__)


@mod.route('/')
def index():
    return {"message": "Hi. This is the API section"}


# #### Users #####


@mod.route('/users', methods=['GET'])
def get_users():
    """ Return all users in our database"""
    users = db.session.query(User).all()
    response = {
        'users': [u.to_dict() for u in users]
    }
    return jsonify(response)


@mod.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """ Return a single, targeted user"""
    try:
        user = db.session.query(User).filter(User.id == id).first()
        return jsonify(user.to_dict())
    except AttributeError as e:
        return invalid_get_target()


@mod.route('/users', methods=['POST'])
def create_user():
    """ Create a new user in our database"""
    data = request.get_json() or {}
    if 'first_name' not in data or 'last_name' not in data or 'email' not in data or 'password' not in data:
        return bad_request('missing required fields: first_name, last_name, email, password')
    if db.session.query(User).filter_by(email=data['email']).first():
        return bad_request('email taken. Please use another.')
    user = User()
    user.from_dict(data)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    return response


@mod.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    """ Modify an existing user in our database"""
    data = request.get_json() or {}
    user = db.session.query(User).filter(User.id == id).first()
    if user is None:
        return invalid_get_target()
    if 'email' in data and db.session.query(User).filter_by(email=data['email']).first():
        return bad_request('email taken. Please use another.')
    print(user)
    user.from_dict(data)
    print(user)
    db.session.commit()
    return jsonify(user.to_dict())

# #### Books #####


@mod.route('/books', methods=['GET'])
def get_books():
    """ Return all books in our database"""
    books = db.session.query(Book).all()
    response = {
        'books': [b.to_dict() for b in books]
    }
    return response


@mod.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    """ Return a single, targeted book"""
    try:
        book = db.session.query(Book).filter(Book.id == id).first()
        return book.to_dict()
    except AttributeError as e:
        return invalid_get_target()


@mod.route('books', methods=['POST'])
def create_book():
    """ Create a new book in our database"""
    data = request.get_json() or {}
    print(data)
    if 'title' not in data or 'author_id' not in data or 'isbn' not in data or 'year_published' not in data:
        return bad_request('missing required fields: author_id, isbn, year_published')
    if db.session.query(Book).filter_by(isbn=data['isbn']).first() or \
       db.session.query(Book).filter_by(title=data['title']).first():
        return bad_request('That book already exists in this database.')
    if db.session.query(Author).filter_by(id=data['author_id']).first is None:
        return bad_request("That author's not in our system. Add the author first.")
    book = Book()
    book.from_dict(data)
    db.session.add(book)
    db.session.commit()
    response = jsonify(book.to_dict())
    response.status_code = 201
    return response


# #### Authors #####


@mod.route('authors', methods=['GET'])
def get_authors():
    """ Return all books in our database"""
    authors = db.session.query(Author).all()
    response = {
        'authors': [a.to_dict() for a in authors]
    }
    return response


@mod.route('/authors/<int:id>', methods=['GET'])
def get_author(id):
    """ Return a single, targeted author"""
    try:
        author = db.session.query(Author).filter(Author.id == id).first()
        return author.to_dict()
    except AttributeError as e:
        return invalid_get_target()


@mod.route('authors', methods=['POST'])
def create_author():
    data = request.get_json() or {}
    if 'first_name' not in data or 'last_name' not in data:
        return bad_request('missing required fields: first_name, last_name')
    author = Author()
    author.from_dict(data)
    db.session.add(author)
    db.session.commit()
    response = jsonify(author.to_dict())
    response.status_code = 201
    return response


# #### Wishlists #####


@mod.route('wishlists', methods=['GET'])
def get_wishlists():
    wishlists = db.session.query(Wishlist).all()
    response = {
        'wishlists': [w.to_dict() for w in wishlists]
    }
    return response


@mod.route('/users/<int:id>/wishlist/<int:book_id>', methods=['POST'])
def add_book_to_wishlist(id, book_id):
    if not db.session.query(User).filter(User.id == id).first():
        return bad_request(f"A user with id {id} does not exist.")
    if not db.session.query(Book).filter(Book.id == book_id).first():
        return bad_request(f"A book with id {book_id} does not exist.")
    if db.session.query(Wishlist).filter(Wishlist.user_id == id, Wishlist.book_id == book_id).first():
        return bad_request("That book is already on this reader's wishlist.")
    else:
        wishlist = Wishlist()
        wishlist.user_id = id
        wishlist.book_id = book_id
        db.session.add(wishlist)
        db.session.commit()
        response = jsonify(f"Success! {book_id} has been added to {id}'s wishlist.")
        response.status_code = 201
        return response


@mod.route('/users/<int:id>/wishlist/<int:book_id>', methods=['DELETE'])
def remove_book_from_wishlist(id, book_id):
    if not db.session.query(User).filter(User.id == id).first():
        return bad_request(f"A user with id {id} does not exist.")
    if not db.session.query(Book).filter(Book.id == book_id).first():
        return bad_request(f"A book with id {book_id} does not exist.")
    if not db.session.query(Wishlist).filter(Wishlist.user_id == id, Wishlist.book_id == book_id).first():
        return bad_request("That book isn't on this reader's wishlist.")
    else:
        db.session.query(Wishlist).filter(Wishlist.user_id == id, Wishlist.book_id == book_id).delete(synchronize_session=False)
        db.session.commit()
        response = jsonify(f"Success! {book_id} has been removed from {id}'s wishlist.'")
        response.status_code = 201
        return response
