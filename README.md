# Book Wishlist Manager

This is an API for allowing a user to view and manage readers' book wishlists.

## Assignment

Create a RESTful API in Python to manage a user's book wish list. Feel free to use any web framework or other tools of your choice, in Python. This includes any database of your choice, though we would recommend SQLite for portability.
 
We would like to see API calls to add, update, and remove books from a user's wish list.
 
For convenience, we have included what attributes users and books should have:

* User
* first_name
* last_name
* email
* password
* Book
* title
* author
* isbn
* date of publication

Tests are highly recommended.
 
Please also include a brief write-up of design and technology choices. This assignment is intentionally light to highlight code style, organization and design choices.

## Usage

Clone this repository.
Create a virtual environment in your local working directory. Activate the virtualenv through the activation script
```bash 
pip install virtualenv
python -m venv venv
venv/scripts/activate
```
Navigate to wishlist_app folder. Install requirements.
```bash
pip install -r requirements.txt
```
From the wishlist_app folder, run the app:
```bash
python wsgi.py
```

