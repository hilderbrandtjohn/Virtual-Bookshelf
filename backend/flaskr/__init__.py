from crypt import methods
import os
from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy  
from flask_cors import CORS
import random

from models import setup_db, Book

#Constant set to enable easy change of books per page or per shelf
BOOKS_PER_SHELF = 8

#Takes request because we can use its arguments to get the page number or 1 if its not  included
def paginate_books(request, books):
    page=request.args.get("page",1,type=int)
    start=(page-1) * BOOKS_PER_SHELF
    end=start + BOOKS_PER_SHELF
    
    #Use list entapolation to format the books appropriately
    formatted_books=[book.format() for book in books]
    #return only the set of books i want to the user for this specific request
    parginated_books= formatted_books[start:end]

    return parginated_books

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    #route that retrivies all books, paginated.
    @app.route('/books')
    def get_books():
        #A query to books,ordered by their id and collected ,all of them
        books=Book.query.order_by(Book.id).all()
        #Helper method which will take request and books
        parginated_books = paginate_books(request, books)

        #if user gives a page that is out of range where we still have books
        if len(parginated_books) == 0:
            abort(404)
        else:

            return jsonify(
                {
                    "success":True,
                    "books":parginated_books,
                    "total_books":len(Book.query.all())
                }
            )
    
    #route that updates rating of one book
    @app.route("/books/<int:book_id>", methods=["PATCH"])
    def update_book(book_id):
        
        #get the body from the request
        body = request.get_json()
        
        #Use try and except so that if there is any failure in finding that book or  being able to update it we send an error
        try:
            #find the book,one or none
            book = Book.query.filter(Book.id == book_id).one_or_none()
            
            #if there is no book for that id ,we abort(404)
            if book is None:
                abort(404)
            
            if "rating" in body:
                #set the book rating to be an integer of body.get("rating")
                #Type cohersion is used to get rating to be an interger because the rating in body is going to come through as string
                book.rating = int(body.get("rating"))

            book.update()

            return jsonify(
                {
                    "success":True, 
                    #tells user which book is updated
                    "id": book.id
                    }
                    )
        except:
            abort(400)

    
    #route that deletes a book
    @app.route("/books/<int:book_id>", methods=["DELETE"])
    def delete_book(book_id):
        try:
            #find the book,one or none
            book=Book.query.filter(Book.id == book_id).one_or_none()

            if book is None:
                abort(404)
            
            #delete book
            book.delete()
            #Find the selection of ordered books
            books=Book.query.order_by(Book.id).all()
            #paginate based on our current location
            parginated_books =paginate_books(request, books)

            return jsonify(
                {
                    "success":True,
                    "deleted":book_id,
                    "books": parginated_books,
                    "total_books":len(Book.query.all()),
                }
            )
        except:
            abort(422)
    
    #route that adds a new book
    @app.route("/books", methods=["POST"])
    def create_book():
        #get the body from the request
        body =request.get_json()
        
        #get the title, author, and rating if they exist
        new_title = body.get("title",None)
        new_author =body.get("author",None)
        new_rating =body.get("rating",None)

        try:
            #create a book
            book =Book(title=new_title, author=new_author,rating=new_rating )
            #insert the book into the database
            book.insert()

            books =Book.query.order_by(Book.id).all()
            parginated_books= paginate_books(request, books)

            return jsonify(
                {
                    "success":True,
                    "created":book.id,
                    "books":parginated_books,
                    "total_books": len(Book.query.all()),
                }
            )
        except:
            abort(422)
    
    #return a useful, formatted response to users that can be parsed the same way as successful requests

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success":False,
                "error":404,
                "message":"resourse not found",
            }
        ),404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {
                "success":False,
                "error":400,
                "message":"bad request",
            }
        ),400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {
                "success":False,
                "error":422,
                "message":"unprocessable",
            }
        ),422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify(
            {
                "success":False,
                "error":405,
                "message":"method not allowed",
            }
        ),405



    return app
