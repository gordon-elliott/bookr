#  __copyright__ = "Copyright (c) 2020 Gordon Elliott"

from sqlalchemy import create_engine

from acme.bookr.db.session_scope import Session

engine = create_engine('sqlite:///bookr.db', echo=True)
Session.configure(bind=engine)
