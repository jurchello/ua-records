from __future__ import annotations

from typing import Any, List

from gramps.gen.lib import Name

from repositories.base_repository import BaseRepository


class NameRepository(BaseRepository):

    def get_first_name(self, name: Name) -> str:
        return name.get_first_name()

    def get_type(self, name: Name) -> Any:
        return name.get_type()

    def get_surname_list(self, name: Name) -> List[Any]:
        return name.get_surname_list()

    def get_surname_list_copy(self, name: Name) -> List[Any]:
        return name.get_surname_list_copy()

    def get_surname(self, name: Name) -> str:
        return name.get_surname()
