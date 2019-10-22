from application import create_app
from os import path

# Create a sample db populated with initial data to play with
if not path.isfile('book_wishlists.db'):
    import sys
    sys.path.append("..")
    import init_demo_db

app = create_app()

if __name__ == "__main__":
    print("*********************************")
    app.run()
