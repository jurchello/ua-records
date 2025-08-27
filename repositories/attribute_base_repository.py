from __future__ import annotations
from typing import List
from gramps.gen.lib import AttributeBase, Attribute

from repositories.base_repository import BaseRepository


class AttributeBaseRepository(BaseRepository):
    
    def get_attribute_list(self, obj: AttributeBase) -> List[Attribute]:
        return obj.get_attribute_list()