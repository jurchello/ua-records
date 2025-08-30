from __future__ import annotations

from typing import Any, List, Tuple

from gramps.gen.lib import BaseObject

from repositories.base_repository import BaseRepository


class BaseObjectRepository(BaseRepository):

    def get_handle_referents(self, obj: BaseObject) -> List[Any]:
        return obj.get_handle_referents()

    def get_referenced_handles(self, obj: BaseObject) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    def get_referenced_handles_recursively(self, obj: BaseObject) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles_recursively()

    def get_text_data_child_list(self, obj: BaseObject) -> List[Any]:
        return obj.get_text_data_child_list()

    def get_text_data_list(self, obj: BaseObject) -> List[str]:
        return obj.get_text_data_list()

    def matches_regexp(self, obj: BaseObject, pattern: str, case_sensitive: bool = False) -> bool:
        return obj.matches_regexp(pattern, case_sensitive)

    def matches_string(self, obj: BaseObject, pattern: str, case_sensitive: bool = False) -> bool:
        return obj.matches_string(pattern, case_sensitive)
