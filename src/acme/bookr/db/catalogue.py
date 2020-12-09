#  __copyright__ = "Copyright (c) 2020 Gordon Elliott"

from acme.bookr.db.mapping import Book
from acme.bookr.db.session_scope import session_scope

TITLES = (
    "The Great Gatsby",
    "Moby-Dick",
    "To Kill a Mockingbird",
    "The Adventures of Huckleberry Finn",
    "Mason & Dixon",
    "American Psycho",
    "Of Mice and Men",
    "The Grapes of Wrath",
    "The Old Man and the Sea",
)


def create_catalogue():
    with session_scope() as session:
        for title in TITLES:
            book = Book(title)
            session.add(book)
        session.flush()
