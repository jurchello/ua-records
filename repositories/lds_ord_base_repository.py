from __future__ import annotations
from typing import List, Any
from gramps.gen.lib import LdsOrdBase

from repositories.base_repository import BaseRepository


class LdsOrdBaseRepository(BaseRepository):
    
    def get_lds_ord_list(self, obj: LdsOrdBase) -> List[Any]:
        return obj.get_lds_ord_list()
    
    def add_lds_ord(self, obj: LdsOrdBase, lds_ord: Any) -> None:
        obj.add_lds_ord(lds_ord)
    
    def remove_lds_ord(self, obj: LdsOrdBase, lds_ord: Any) -> bool:
        return obj.remove_lds_ord(lds_ord)
    
    def set_lds_ord_list(self, obj: LdsOrdBase, lds_ord_list: List[Any]) -> None:
        obj.set_lds_ord_list(lds_ord_list)