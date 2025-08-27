from __future__ import annotations
from typing import List, Any
from gramps.gen.lib import AddressBase

from repositories.base_repository import BaseRepository


class AddressBaseRepository(BaseRepository):
    
    def get_address_list(self, obj: AddressBase) -> List[Any]:
        return obj.get_address_list()
    
    def add_address(self, obj: AddressBase, address: Any) -> None:
        obj.add_address(address)
    
    def remove_address(self, obj: AddressBase, address: Any) -> bool:
        return obj.remove_address(address)
    
    def set_address_list(self, obj: AddressBase, address_list: List[Any]) -> None:
        obj.set_address_list(address_list)