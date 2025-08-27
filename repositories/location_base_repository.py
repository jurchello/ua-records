from __future__ import annotations
from typing import Any
from gramps.gen.lib import LocationBase

from repositories.base_repository import BaseRepository


class LocationBaseRepository(BaseRepository):
    
    def get_main_location(self, obj: LocationBase) -> Any:
        return obj.get_main_location()
    
    def set_main_location(self, obj: LocationBase, location: Any) -> None:
        obj.set_main_location(location)