from __future__ import annotations
from typing import Any
from gramps.gen.db.base import DbReadBase


class BaseRepository:
    """Base repository class providing database access for all repositories."""
    
    def __init__(self, db: DbReadBase) -> None:
        self.db = db