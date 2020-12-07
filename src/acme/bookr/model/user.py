

class User:
    _email: str

    def __init__(self, email):
        self._email = email

    @property
    def email(self) -> str:
        return self._email
