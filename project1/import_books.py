import csv
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from app.models import Book

def main():
    with open('books.csv','r') as bookfile:
        booklist = csv.reader(bookfile)
        next(booklist)
        num = 1
        for row in booklist:
            book = Book(isbn=row[0], book_title=row[1], author=row[2], year=row[3])
            db.session.add(book)
            db.session.commit()
            print(f'{num} {book.book_title}')
            num += 1
            
if __name__ == "__main__":
    main()