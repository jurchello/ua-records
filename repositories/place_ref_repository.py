from __future__ import annotations

from gramps.gen.lib import PlaceRef

from repositories.base_repository import BaseRepository


class PlaceRefRepository(BaseRepository):

    def get_reference_handle(self, place_ref: PlaceRef) -> str:
        return place_ref.get_reference_handle()

    def set_reference_handle(self, place_ref: PlaceRef, handle: str) -> None:
        place_ref.set_reference_handle(handle)
