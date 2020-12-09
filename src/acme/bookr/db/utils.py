#  __copyright__ = "Copyright (c) 2020 Gordon Elliott"

from contextlib import closing

from acme.bookr.db.mapping import book_request, user


def truncate_operational_tables(engine):
    with closing(engine.connect()) as connection:
        transaction = connection.begin()
        connection.execute(book_request.delete())
        connection.execute(user.delete())
        transaction.commit()
