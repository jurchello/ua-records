from __future__ import annotations

from gramps.gen.lib import GrampsType

from repositories.base_repository import BaseRepository


class GrampsTypeRepository(BaseRepository):

    def get_string(self, gramps_type: GrampsType) -> str:
        return gramps_type.get_string()

    def set_string(self, gramps_type: GrampsType, value: str) -> None:
        gramps_type.set_string(value)

    def is_custom(self, gramps_type: GrampsType) -> bool:
        return gramps_type.is_custom()

    def is_default(self, gramps_type: GrampsType) -> bool:
        return gramps_type.is_default()
