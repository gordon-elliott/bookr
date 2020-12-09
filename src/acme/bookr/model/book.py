#  __copyright__ = "Copyright (c) 2020 Gordon Elliott"

class Book:
    _title: str

    def __init__(self, title: str):
        self._title = title

    @property
    def title(self) -> str:
        return self._title
