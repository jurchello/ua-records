from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gramps.gen.db.base import DbReadBase


class RepositoryCore:
    def __init__(self, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = db
