from __future__ import annotations
from typing import Iterable
from repositories.base_repository import BaseRepository

class BacklinkRepository(BaseRepository):
    def find_backlinks(self, handle: str, objtype: str) -> list[tuple[str, object]]:
        raw: Iterable[tuple[str, object]] = self.db.find_backlink_handles(handle, objtype)
        return list(raw)