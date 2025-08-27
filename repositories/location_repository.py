from __future__ import annotations
from gramps.gen.lib import Location

from repositories.base_repository import BaseRepository


class LocationRepository(BaseRepository):
    
    def get_street(self, location: Location) -> str:
        return location.get_street()
    
    def get_locality(self, location: Location) -> str:
        return location.get_locality()
    
    def get_city(self, location: Location) -> str:
        return location.get_city()
    
    def get_county(self, location: Location) -> str:
        return location.get_county()
    
    def get_state(self, location: Location) -> str:
        return location.get_state()
    
    def get_country(self, location: Location) -> str:
        return location.get_country()
    
    def get_postal(self, location: Location) -> str:
        return location.get_postal()
    
    def get_phone(self, location: Location) -> str:
        return location.get_phone()
    
    def is_empty(self, location: Location) -> bool:
        return location.is_empty()