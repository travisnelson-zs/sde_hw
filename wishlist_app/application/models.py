from flask_sqlalchemy import SQLAlchemy
from operator import attrgetter
import time

db = SQLAlchemy()


class Wishlist(db.Model):
    __tablename__ = 'wishlists'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
    last_updated = db.Column(db.String(11), nullable=False, default=int(time.time()))
    reader = db.relationship('User', back_populates='books')
    book = db.relationship('Book', back_populates='readers')

    def to_dict(self):
        data = {
            'user_id': self.user_id,
            'book_id': self.book_id,
            'last_updated': self.last_updated
        }
        return data


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    books = db.relationship('Wishlist', back_populates='reader')

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}', '{self.password}')"

    def to_dict(self):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'wishlist': {
                'total_count': len(self.books),
                'books': [i.book.to_dict(hide_wishlists=True) for i in self.books]
            }
        }
        return data

    def from_dict(self, data):
        for field in ['first_name', 'last_name', 'email', 'password']:
            if field in data:
                setattr(self, field, data[field])


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'),
                          nullable=False)
    title = db.Column(db.String(120), unique=True, nullable=False)
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    readers = db.relationship("Wishlist", back_populates="book")

    def __repr__(self):
        return f"Book('{self.title}', '{self.author_id}',\
                      '{self.isbn}', '{self.year_published}')"

    def to_dict(self, hide_author=False, hide_wishlists=False):
        data = {
            'id': self.id,
            'title': self.title,
            'isbn': self.isbn,
            'year_published': self.year_published,
        }
        if not hide_author:
            data['author_id'] = self.author_id
        if not hide_wishlists:
            data['wishlists'] = {
                'count': len(self.readers),
                'user_ids': [i.user_id for i in self.readers]
            }
        return data

    def from_dict(self, data):
        for field in ['author_id', 'title', 'isbn', 'year_published']:
            if field in data:
                setattr(self, field, data[field])


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=True)
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return f"Author('{self.first_name}, '{self.last_name}')"

    def to_dict(self):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'books': [b.to_dict(hide_author=True, hide_wishlists=True) for b in self.books]
        }
        return data

    def from_dict(self, data):
        for field in ['first_name', 'last_name']:
            if field in data:
                setattr(self, field, data[field])
