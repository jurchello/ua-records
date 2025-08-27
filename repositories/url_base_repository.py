from __future__ import annotations
from typing import List, Any
from gramps.gen.lib import UrlBase

from repositories.base_repository import BaseRepository


class UrlBaseRepository(BaseRepository):
    
    def get_url_list(self, obj: UrlBase) -> List[Any]:
        return obj.get_url_list()
    
    def add_url(self, obj: UrlBase, url: Any) -> None:
        obj.add_url(url)
    
    def remove_url(self, obj: UrlBase, url: Any) -> bool:
        return obj.remove_url(url)
    
    def set_url_list(self, obj: UrlBase, url_list: List[Any]) -> None:
        obj.set_url_list(url_list)