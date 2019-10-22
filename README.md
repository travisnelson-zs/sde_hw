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

## Road Map

* Tests. Lots of tests.
* Password hashing. Use PassLib?
* Site UI, including forms to add/remove/update Users, Books, Authors, Wishlists
* Additional error handling 


## Write Up

This assignment has been a huge learning experience for me. While I both regularly use API’s and query tables, I’d never previously created either.  I started by reading up on sqlite. I knew I’d need a User table and a Book table, with columns representing the attributes laid out in the assignment. As I continued reading about databases, the term ‘normalization’ came up a lot. I wanted to design my tables correctly, and a design technique that seeks to reduce redundancy and dependency of data seemed like the right way to go. That led me to create two additional tables: ‘authors’ and ‘wishlists’. Once I had my tables created, I wanted to populate them with some initial data, so they’d be more fun to play with. I made a csv full of sample data for each table and wrapped the open/read/insert process in a function. I put all associated files into a folder that I turned into a package. This allowed me to be able to create a populated book-wishlist database on command.

 
At the same time, I was researching Python web frameworks. I’d previously heard of/read a bit on Flask and Django, and after a bit more googling, Flask seemed like the right tool. I liked that it was ‘lightweight’, and its Quickstart guide understandable. I also came across a heavily-referenced Flask Mega Tutorial by Miguel Grinberg that seemed like it’d be a great resource. I began building out my app, creating endpoints with placeholder values, and playing with render_template(). I had to figure out a good way to manage my database, which led me to SQLAlchemy, which I learned is an Object Relational Mapper (ORM). “ORMs allow applications to manage a database using high-level entities such as classes, objects and methods instead of tables and SQL.” This seemed like a good match for my project. I connected the SQLALCHEMY_DATABASE_URI to my book_wishlist.db and created models for each table that matched the schema of the db. I think there are a few other ways I could have gone about configuring the relationship, but I went with this one. 

My project was getting kind of messy, and as I read more and watched more guides and tutorials, I began to suspect it wasn’t structured in a scalable, professional way. I read about a design pattern called the “Flask application factory”, which makes it easier to create multiple instances of the app. Even though it wasn’t necessary for this project, there were enough references to it being the preferred design pattern that I thought I should give it a shot.

Then I realized I actually needed to complete the assignment, which meant I had to get my API working! I set up endpoints in my API blueprint and tested to make sure they returned something. Because SQLAlchemy models are also classes, I was able to create methods that returned instance information in dict form, which could then be converted to json and returned.  SQLAlchemy made this really convenient, because I was able to query the table(s) and return either a model class instance, or a collection (which could be iterated over).

In addition to my API blueprint, I’d also made a ‘site’ blueprint, which I imagined to be used for by users to view user/book/wishlist data in-browser. I only got around to making the index/home page (with bare minimum CSS), but the framework is laid for building out forms to allow users to manipulate the db. Currently, the homepage provides directions on how to use the API. 
