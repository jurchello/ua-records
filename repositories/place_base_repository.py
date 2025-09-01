from __future__ import annotations

from gramps.gen.lib import PlaceBase

from repositories.repository_core import RepositoryCore


class PlaceBaseRepository(RepositoryCore):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_place_handle(self, obj: PlaceBase) -> str:
        return obj.get_place_handle()

    def set_place_handle(self, obj: PlaceBase, place_handle: str) -> None:
        obj.set_place_handle(place_handle)

    def place_handle(self, obj: PlaceBase) -> str:
        try:
            return obj.place_handle
        except AttributeError:
            return obj.get_place_handle()
