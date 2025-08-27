from __future__ import annotations
from typing import Any
from gramps.gen.lib import Attribute

from repositories.base_repository import BaseRepository


class GrampsAttributeRepository(BaseRepository):
    
    def get_type(self, attribute: Attribute) -> Any:
        return attribute.get_type()
    
    def get_value(self, attribute: Attribute) -> str:
        return attribute.get_value()