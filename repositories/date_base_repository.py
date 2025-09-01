from __future__ import annotations
from typing import Any

from gramps.gen.lib import Date, DateBase

from repositories.repository_core import RepositoryCore


class DateBaseRepository(RepositoryCore):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_date_object(self, obj: DateBase) -> Date:
        return obj.get_date_object()

    def set_date_object(self, obj: DateBase, date: Date) -> None:
        obj.set_date_object(date)

    def serialize(self, obj: DateBase, no_text_date: bool = False) -> Any:
        return obj.serialize(no_text_date=no_text_date)

    def unserialize(self, obj: DateBase, data: Any) -> None:
        obj.unserialize(data)
