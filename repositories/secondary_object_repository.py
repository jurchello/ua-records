from __future__ import annotations
from typing import Any
from gramps.gen.lib import SecondaryObject

from repositories.base_object_repository import BaseObjectRepository


class SecondaryObjectRepository(BaseObjectRepository):
    
    def is_equal(self, obj: SecondaryObject, other: Any) -> bool:
        return obj.is_equal(other)
    
    def is_equivalent(self, obj: SecondaryObject, other: Any) -> bool:
        return obj.is_equivalent(other)