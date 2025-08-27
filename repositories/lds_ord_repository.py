from __future__ import annotations
from typing import Any
from gramps.gen.lib import LdsOrd

from repositories.base_repository import BaseRepository


class LdsOrdRepository(BaseRepository):
    
    def get_type(self, lds_ord: LdsOrd) -> Any:
        return lds_ord.get_type()
    
    def get_temple(self, lds_ord: LdsOrd) -> str:
        return lds_ord.get_temple()
    
    def get_status(self, lds_ord: LdsOrd) -> int:
        return lds_ord.get_status()
    
    def get_family_handle(self, lds_ord: LdsOrd) -> str:
        return lds_ord.get_family_handle()
    
    def is_empty(self, lds_ord: LdsOrd) -> int:
        return lds_ord.is_empty()