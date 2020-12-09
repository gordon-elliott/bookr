#  __copyright__ = "Copyright (c) 2020 Gordon Elliott"

import pytest

from acme.bookr.model import User
from acme.bookr.model.user import InvalidEmailError


@pytest.mark.parametrize(
    "email",
    (
        "jb@example.com",
        "joe.x.bloggs@unit.dept.example.com",
        "21222@numeric.org",
        "ALL_CAPS@shouting.us",
        "a@b.it"
    )
)
def test_email_valid(email):
    user = User(email)
    assert user is not None
    assert user.email == email


@pytest.mark.parametrize(
    "email",
    (
        "",
        "bad@@email.com",
        "worse@e@mail.com",
        "no_at.email.com",
        "joe@no_tld"
    )
)
def test_email_invalid(email):
    with pytest.raises(InvalidEmailError):
        User(email)
