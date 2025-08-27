from __future__ import annotations
from typing import Any
from gramps.gen.lib import PlaceName

from repositories.base_repository import BaseRepository
from repositories.date_base_repository import DateBaseRepository


class PlaceNameRepository(BaseRepository, DateBaseRepository):
    
    def get_value(self, place_name: PlaceName) -> str:
        return place_name.get_value()
    
    def get_language(self, place_name: PlaceName) -> str:
        return place_name.get_language()
    
    def set_value(self, place_name: PlaceName, value: str) -> None:
        place_name.set_value(value)
    
    def set_language(self, place_name: PlaceName, language: str) -> None:
        place_name.set_language(language)