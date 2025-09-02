from __future__ import annotations

from typing import Any, List, Optional, Tuple

from gramps.gen.lib import Surname

from repositories.repository_core import RepositoryCore


class SurnameBaseRepository(RepositoryCore):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def add_surname(self, obj, surname: Surname) -> None:
        obj.add_surname(surname)

    def get_connectors(self, obj) -> List[str]:
        return obj.get_connectors()

    def get_prefixes(self, obj) -> List[str]:
        return obj.get_prefixes()

    def get_primary_surname(self, obj) -> Optional[Surname]:
        return obj.get_primary_surname()

    def get_surname(self, obj) -> str:
        return obj.get_surname()

    def get_surname_list(self, obj) -> List[Surname]:
        return obj.get_surname_list()

    def get_surnames(self, obj) -> List[str]:
        return obj.get_surnames()

    def get_upper_surname(self, obj) -> str:
        return obj.get_upper_surname()

    def remove_surname(self, obj, surname: Surname) -> bool:
        return obj.remove_surname(surname)

    def set_primary_surname(self, obj, surnamenr: int = 0) -> None:
        obj.set_primary_surname(surnamenr)

    def set_surname_list(self, obj, surname_list: List[Surname]) -> None:
        obj.set_surname_list(surname_list)

    def serialize(self, obj) -> Tuple[Any, ...]:
        return obj.serialize()

    def unserialize(self, obj, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)
