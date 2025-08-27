from __future__ import annotations
from typing import List, Any
from gramps.gen.lib.attribute import AttributeRoot

from repositories.base_repository import BaseRepository


class AttributeRootRepository(BaseRepository):
    
    def get_type(self, attr: AttributeRoot) -> Any:
        return attr.get_type()
    
    def get_value(self, attr: AttributeRoot) -> str:
        return attr.get_value()
    
    def set_type(self, attr: AttributeRoot, attr_type: Any) -> None:
        attr.set_type(attr_type)
    
    def set_value(self, attr: AttributeRoot, value: str) -> None:
        attr.set_value(value)