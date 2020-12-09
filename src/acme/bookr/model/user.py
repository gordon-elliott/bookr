#  __copyright__ = "Copyright (c) 2020 Gordon Elliott"

import re

# simple, pragmatic format check on email address
VALID_EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"


class InvalidEmailError(Exception):
    pass


class User:
    _email: str

    def __init__(self, email):
        self.email = email

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value):
        if re.fullmatch(VALID_EMAIL_REGEX, value):
            self._email = value
        else:
            raise InvalidEmailError(f"Invalid email address '{value}'")
