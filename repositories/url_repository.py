from __future__ import annotations
from typing import Any
from gramps.gen.lib import Url

from repositories.base_repository import BaseRepository


class UrlRepository(BaseRepository):
    
    def get_path(self, url: Url) -> str:
        return url.get_path()
    
    def get_description(self, url: Url) -> str:
        return url.get_description()
    
    def get_type(self, url: Url) -> Any:
        return url.get_type()
    
    def set_path(self, url: Url, path: str) -> None:
        url.set_path(path)
    
    def set_description(self, url: Url, description: str) -> None:
        url.set_description(description)
    
    def set_type(self, url: Url, url_type: Any) -> None:
        url.set_type(url_type)