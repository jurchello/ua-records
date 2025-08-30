from __future__ import annotations

from gramps.gen.lib import EventRef

from repositories.base_repository import BaseRepository


class EventRefRepository(BaseRepository):

    def get_reference_handle(self, event_ref: EventRef) -> str:
        return event_ref.get_reference_handle()

    def get_role(self, event_ref: EventRef) -> str:
        return event_ref.get_role()
