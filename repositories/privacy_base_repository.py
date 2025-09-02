from __future__ import annotations
from typing import Any, Tuple


from repositories.repository_core import RepositoryCore


class PrivacyBaseRepository(RepositoryCore):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_privacy(self, obj) -> bool:
        return obj.get_privacy()

    def set_privacy(self, obj, val: bool) -> None:
        obj.set_privacy(val)

    def serialize(self, obj) -> Tuple[Any, ...]:
        return obj.serialize()

    def unserialize(self, obj, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)
