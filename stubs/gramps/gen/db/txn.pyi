from __future__ import annotations
from typing import Any, Optional, Type

from gramps.gen.db.base import DbReadBase

class DbTxn:
    def __init__(self, label: str, db: DbReadBase) -> None: ...
    def __enter__(self) -> "DbTxn": ...
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Any,
    ) -> None: ...