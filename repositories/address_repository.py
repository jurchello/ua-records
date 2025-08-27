from __future__ import annotations
from typing import List, Any
from gramps.gen.lib import Address

from repositories.base_repository import BaseRepository


class AddressRepository(BaseRepository):
    
    def get_street(self, address: Address) -> str:
        return address.get_street()
    
    def get_locality(self, address: Address) -> str:
        return address.get_locality()
    
    def get_city(self, address: Address) -> str:
        return address.get_city()
    
    def get_county(self, address: Address) -> str:
        return address.get_county()
    
    def get_state(self, address: Address) -> str:
        return address.get_state()
    
    def get_country(self, address: Address) -> str:
        return address.get_country()
    
    def get_postal_code(self, address: Address) -> str:
        return address.get_postal_code()
    
    def get_phone(self, address: Address) -> str:
        return address.get_phone()