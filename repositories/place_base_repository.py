from __future__ import annotations
from gramps.gen.lib import PlaceBase

from repositories.base_repository import BaseRepository


class PlaceBaseRepository(BaseRepository):
    
    def get_place_handle(self, obj: PlaceBase) -> str:
        return obj.get_place_handle()