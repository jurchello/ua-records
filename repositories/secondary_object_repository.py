from __future__ import annotations

from typing import Any, Tuple

from gramps.gen.lib import SecondaryObject

from repositories.base_object_repository import BaseObjectRepository


class SecondaryObjectRepository(BaseObjectRepository):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def is_equal(self, obj: SecondaryObject, other: Any) -> bool:
        return obj.is_equal(other)

    def is_equivalent(self, obj: SecondaryObject, other: Any) -> Any:
        return obj.is_equivalent(other)

    def serialize(self, obj: SecondaryObject) -> Any:
        return obj.serialize()

    def unserialize(self, obj: SecondaryObject, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)
