from __future__ import annotations
from typing import Iterable, Optional
from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Tag

from repositories.base_repository import BaseRepository

class TagRepository(BaseRepository):

    def get_by_handle(self, handle: str) -> Optional[Tag]:
        return self.db.get_tag_from_handle(handle)

    def add(self, tag: Tag, description: str = "Add tag") -> str:
        with DbTxn(description, self.db) as trans:
            return self.db.add_tag(tag, trans)
    
    def commit(self, tag: Tag, description: str = "Update tag") -> None:
        with DbTxn(description, self.db) as trans:
            self.db.commit_tag(tag, trans)
    
    def find_by_name(self, name: str) -> Optional[Tag]:
        for h in self.db.get_tag_handles():
            t = self.db.get_tag_from_handle(h)
            if t and t.get_name() == name:
                return t
        return None
    
    def get_handles(self) -> Iterable[str]:
        return self.db.get_tag_handles()