from __future__ import annotations
from typing import Optional
from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Family

from repositories.base_repository import BaseRepository


class FamilyRepository(BaseRepository):

    def get_by_handle(self, handle: str) -> Optional[Family]:
        return self.db.get_family_from_handle(handle)

    def add(self, family: Family, description: str = "Add family") -> str:
        with DbTxn(description, self.db) as trans:
            return self.db.add_family(family, trans)

    def commit(self, family: Family, description: str = "Update family") -> None:
        with DbTxn(description, self.db) as trans:
            self.db.commit_family(family, trans)