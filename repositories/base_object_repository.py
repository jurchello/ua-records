from __future__ import annotations

from typing import Any, List, Tuple

from gramps.gen.lib import BaseObject

from repositories.repository_core import RepositoryCore


class BaseObjectRepository(RepositoryCore):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_handle_referents(self, obj: BaseObject) -> List[Any]:
        return obj.get_handle_referents()

    def get_referenced_handles(self, obj: BaseObject) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    def get_referenced_handles_recursively(self, obj: BaseObject) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles_recursively()

    def get_text_data_child_list(self, obj: BaseObject) -> List[Any]:
        return obj.get_text_data_child_list()

    def get_text_data_list(self, obj: BaseObject) -> List[str | None]:
        return obj.get_text_data_list()

    def matches_regexp(self, obj: BaseObject, pattern: str, case_sensitive: bool = False) -> bool:
        return obj.matches_regexp(pattern, case_sensitive)

    def matches_string(self, obj: BaseObject, pattern: str, case_sensitive: bool = False) -> bool:
        return obj.matches_string(pattern, case_sensitive)

    def merge(self, obj: BaseObject, acquisition: BaseObject) -> None:
        obj.merge(acquisition)

    def serialize(self, obj: BaseObject) -> Any:
        return obj.serialize()

    def unserialize(self, obj: BaseObject, data: Any) -> None:
        obj.unserialize(data)
