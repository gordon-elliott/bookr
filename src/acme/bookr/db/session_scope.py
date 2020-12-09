#  __copyright__ = "Copyright (c) 2020 Gordon Elliott"

from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

Session = sessionmaker()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as all_exceptions:
        session.rollback()
        from acme.bookr.api import app
        app.logger.error(all_exceptions)
        raise
    finally:
        session.close()
