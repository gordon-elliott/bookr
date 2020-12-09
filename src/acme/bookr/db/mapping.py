#  __copyright__ = "Copyright (c) 2020 Gordon Elliott"

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import mapper, relationship

from acme.bookr.model import User, Book, BookRequest

metadata = MetaData()


def _uuid_str() -> str:
    return str(uuid4())


book_request = Table(
    'book_request',
    metadata,
    Column('id', Integer, primary_key=True, key="_id"),
    Column('uuid', String(36), key="_uuid", default=_uuid_str),
    Column('user_id', Integer, ForeignKey('user._id'), key="_user_id"),
    Column('book_id', Integer, ForeignKey('book._id'), key="_book_id"),
    Column('timestamp', DateTime, key="_timestamp", default=datetime.now)
)

mapper(BookRequest, book_request)

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True, key="_id"),
    Column('email', String(256), key="_email"),
)

mapper(User, user, properties={
    'book_requests': relationship(BookRequest, backref='requester', order_by=book_request.c._timestamp)
})

book = Table(
    'book',
    metadata,
    Column('id', Integer, primary_key=True, key="_id"),
    Column('title', String(256), key="_title"),
)

mapper(Book, book, properties={
    'book_requests': relationship(BookRequest, backref='book', order_by=book_request.c._timestamp)
})
