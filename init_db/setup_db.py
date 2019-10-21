import sqlite3
import csv
import os


def create_tables(connection, cursor):
    sql_command = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            author_id INTEGER NOT NULL,
            title TEXT UNIQUE NOT NULL,
            isbn INTEGER UNIQUE NOT NULL,
            year_published INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES authors(id)
        );
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT
        );
        CREATE TABLE IF NOT EXISTS wishlists (
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            last_updated INTEGER NOT NULL,
            UNIQUE (user_id, book_id) ON CONFLICT REPLACE,
            PRIMARY KEY(user_id, book_id)
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """
    cursor.executescript(sql_command)
    connection.commit()


def populate_tables(connection, cursor):

    basedir = os.path.dirname(os.path.abspath(__file__))

    # I read that string constructors are bad practice, because they create vulnerabilites to SQL
    # injection attacks. I'd like to learn if there's any way to use variables for new table names.

    with open(os.path.join(basedir, 'users.csv'), 'r') as f:
        dr = csv.DictReader(f)
        to_users_table = [(i['first_name'], i['last_name'], i['email'], i['password']) for i in dr]
    cursor.executemany("INSERT OR IGNORE INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?);", to_users_table)

    with open(os.path.join(basedir, 'authors.csv'), 'r') as f:
        dr = csv.DictReader(f)
        to_authors_table = [(i['first_name'], i['last_name']) for i in dr]
    cursor.executemany("INSERT INTO authors (first_name, last_name) VALUES (?, ?);", to_authors_table)

    with open(os.path.join(basedir, 'books.csv'), 'r') as f:
        dr = csv.DictReader(f)
        to_books_table = [(i['author_id'], i['title'], i['isbn'], i['year_published']) for i in dr]
    cursor.executemany("INSERT OR IGNORE INTO books (author_id, title, isbn, year_published) VALUES (?, ?, ?, ?);", to_books_table)

    with open(os.path.join(basedir, 'wishlists.csv'), 'r') as f:
        dr = csv.DictReader(f)
        to_wishlists_table = [(i['user_id'], i['book_id'], i['last_updated']) for i in dr]
    cursor.executemany("INSERT INTO wishlists (user_id, book_id, last_updated) VALUES (?, ?, ?);", to_wishlists_table)

    connection.commit()


def init_bookwishlist_db():
    conn = sqlite3.connect('book_wishlists.db')
    c = conn.cursor()
    create_tables(conn, c)
    populate_tables(conn, c)
    conn.close()
