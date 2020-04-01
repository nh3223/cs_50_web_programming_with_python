import csv
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from app.models import Book

def main():
    with open('books.csv','r') as bookfile:
        booklist = csv.reader(bookfile)
        next(booklist)
        for row in booklist:
            book = Book(isbn=row[0], title=row[1], author=row[2], year=row[3])
            db.session.add(book)
            db.session.commit()

if __name__ == "__main__":
    main()