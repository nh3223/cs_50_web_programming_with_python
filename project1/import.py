import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    with open("books.csv") as bookfile:
        booklist = csv.reader(bookfile)
    for book in booklist:
        db.execute("INSERT INTO books (origin, destination, duration) VALUES (:origin, :destination, :duration)",
                   {"origin": origin, "destination": destination, "duration": duration})
    db.commit()

if __name__ == "__main__":
    main()