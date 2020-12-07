from datetime import datetime

import pytest

from acme.bookr.db.engine import engine
from acme.bookr.db.session_scope import session_scope
from acme.bookr.db.catalogue import create_catalogue, TITLES
from acme.bookr.db.mapping import metadata, Book, User, BookRequest


EMAIL_FIXTURE = "jb@example.com"
BOOK_FIXTURE = "To Kill a Mockingbird"


@pytest.fixture(scope='module')
def setup():
    metadata.create_all(engine)
    create_catalogue()

    yield

    metadata.drop_all(engine)


@pytest.fixture(scope='module')
def existing_user():
    with session_scope() as session:
        users = session.query(User).all()

        assert not users

        new_user = User(EMAIL_FIXTURE)
        session.add(new_user)

    yield new_user

    with session_scope() as session:
        session.query(User).delete()

def test_catalogue(setup):
    with session_scope() as session:
        books = session.query(Book).all()

        assert len(TITLES) == len(books)
        assert "Of Mice and Men" in [book.title for book in books]


def test_user(setup, existing_user):

    with session_scope() as sesssion:
        users = sesssion.query(User).all()

        assert len(users) == 1
        assert users[0].email == EMAIL_FIXTURE
        user_id = users[0]._id

        user = sesssion.query(User).get(user_id)

        assert user.email == EMAIL_FIXTURE


def test_book_request(setup, existing_user):

    with session_scope() as session:
        book = session.query(Book).filter_by(_title=BOOK_FIXTURE).one()

        book_request = BookRequest()
        book_request.book = book
        book_request.requester = existing_user
        session.add(book_request)

    with session_scope() as session:
        book_requests = session.query(BookRequest).all()
        assert len(book_requests) == 1
        reread_request = book_requests[0]
        assert len(reread_request.public_id) == 36
        assert isinstance(reread_request.timestamp, datetime)
        assert reread_request.book.title == BOOK_FIXTURE
        assert reread_request.requester.email == EMAIL_FIXTURE
