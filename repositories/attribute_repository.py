from __future__ import annotations

from gramps.gen.lib import Attribute, AttributeType
from repositories.base_repository import BaseRepository


class AttributeRepository(BaseRepository):

    def build(self, attr_type: AttributeType | str, value: str) -> Attribute:
        a = Attribute()
        a.set_type(attr_type)
        a.set_value(value)
        return a