from __future__ import annotations
from typing import Iterator, Optional
from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Event

from repositories.base_repository import BaseRepository


class EventRepository(BaseRepository):

    def get_by_handle(self, handle: str) -> Optional[Event]:
        return self.db.get_event_from_handle(handle)

    def add(self, event: Event, description: str = "Add event") -> str:
        with DbTxn(description, self.db) as trans:
            return self.db.add_event(event, trans)

    def commit(self, event: Event, description: str = "Update event") -> None:
        with DbTxn(description, self.db) as trans:
            self.db.commit_event(event, trans)

    def iter_all(self) -> Iterator[Event]:
        return self.db.iter_events()