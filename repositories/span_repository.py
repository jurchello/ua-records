from __future__ import annotations
from typing import Any, Tuple
from gramps.gen.lib.date import Span
from repositories.repository_core import RepositoryCore

class SpanRepository(RepositoryCore):
    ABOUT = 50
    AFTER = 50
    ALIVE = 110
    BEFORE = 50

    def __init__(self, db=None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def as_age(self, obj) -> int:
        return obj.as_age()

    def as_time(self, obj) -> int:
        return obj.as_time()

    def format(self, obj, precision: int = 2, as_age: bool = True, dlocale: Any = None) -> str:
        return obj.format(precision=precision, as_age=as_age, dlocale=dlocale)

    def get_repr(self, obj, as_age: bool = False, dlocale: Any = None) -> str:
        return obj.get_repr(as_age=as_age, dlocale=dlocale)

    def is_valid(self, obj) -> bool:
        return obj.is_valid()

    def tuple(self, obj) -> Tuple[int, int, int]:
        return obj.tuple()

    def sort(self, obj) -> Tuple[int, int]:
        try:
            return obj.sort
        except AttributeError:
            return (0, 0)

    def minmax(self, obj) -> Tuple[int, int]:
        try:
            return obj.minmax
        except AttributeError:
            return (0, 0)