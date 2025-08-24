from __future__ import annotations
from typing import Optional
from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Place

from repositories.base_repository import BaseRepository


class PlaceRepository(BaseRepository):

    def get_by_handle(self, handle: str) -> Optional[Place]:
        return self.db.get_place_from_handle(handle)
    
    def add(self, place: Place, description: str = "Add place") -> str:
        with DbTxn(description, self.db) as trans:
            return self.db.add_place(place, trans)
    
    def commit(self, place: Place, description: str = "Update place") -> None:
        with DbTxn(description, self.db) as trans:
            self.db.commit_place(place, trans)