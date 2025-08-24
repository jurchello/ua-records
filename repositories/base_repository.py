from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gramps.gen.db.base import DbReadBase

class BaseRepository:
    def __init__(self, db: DbReadBase) -> None:
        self.db: DbReadBase = db