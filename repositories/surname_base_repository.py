from __future__ import annotations
from typing import List, Any
from gramps.gen.lib import SurnameBase

from repositories.base_repository import BaseRepository


class SurnameBaseRepository(BaseRepository):
    
    def get_surname_list(self, obj: SurnameBase) -> List[Any]:
        return obj.get_surname_list()
    
    def get_surname(self, obj: SurnameBase) -> str:
        return obj.get_surname()
    
    def get_primary_surname(self, obj: SurnameBase) -> Any:
        return obj.get_primary_surname()
    
    def get_surnames(self, obj: SurnameBase) -> List[str]:
        return obj.get_surnames()
    
    def get_prefixes(self, obj: SurnameBase) -> List[str]:
        return obj.get_prefixes()
    
    def get_connectors(self, obj: SurnameBase) -> List[str]:
        return obj.get_connectors()
    
    def add_surname(self, obj: SurnameBase, surname: Any) -> None:
        obj.add_surname(surname)
    
    def set_surname_list(self, obj: SurnameBase, surname_list: List[Any]) -> None:
        obj.set_surname_list(surname_list)
    
    def set_primary_surname(self, obj: SurnameBase, surnamenr: int = 0) -> None:
        obj.set_primary_surname(surnamenr)