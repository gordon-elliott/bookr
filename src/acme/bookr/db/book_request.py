from typing import Optional, Dict, List
from uuid import UUID

from acme.bookr.db.session_scope import session_scope
from acme.bookr.db.mapping import Book, User, BookRequest


def create_book_request(requester_email: str, book_title: str) -> Dict[str, str]:
    with session_scope() as session:
        user = session.query(User).filter_by(_email=requester_email).one_or_none()
        if not user:
            user = User(requester_email)
            session.add(user)

        book = session.query(Book).filter_by(_title=book_title).one()

        book_request = BookRequest()
        book_request.book = book
        book_request.requester = user
        session.add(book_request)
        session.flush()

        return book_request.as_dict()


def get_book_request(request_id: UUID) -> Optional[Dict[str, str]]:
    with session_scope() as session:
        book_request = session.query(BookRequest).filter_by(_uuid=str(request_id)).one_or_none()
        return book_request.as_dict()


def list_book_requests() -> List[Dict[str, str]]:
    with session_scope() as session:
        return [book_request.as_dict() for book_request in session.query(BookRequest).all()]


def delete_book_request(request_id: str):
    with session_scope() as session:
        return session.query(BookRequest).filter_by(_uuid=request_id).delete()
