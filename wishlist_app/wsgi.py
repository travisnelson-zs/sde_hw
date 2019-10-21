from application import create_app
from os import path

if not path.isfile('book_wishlists.db'):
    import sys
    sys.path.append("..")
    import init_db

app = create_app()

if __name__ == "__main__":
    print("*********************************")
    app.run()
