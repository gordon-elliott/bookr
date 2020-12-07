from datetime import datetime
from typing import Dict


class BookRequest:
    _timestamp: datetime
    _uuid: str

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def public_id(self) -> str:
        return self._uuid

    def as_dict(self) -> Dict[str, str]:
        return dict(
            email=self.requester.email,
            title=self.book.title,
            id=self._uuid,
            timestamp=self._timestamp.isoformat()
        )
