from __future__ import annotations

from typing import Any, List, Optional, Sequence, Tuple

from gramps.gen.lib.attribute import AttributeRoot

from repositories.privacy_base_repository import PrivacyBaseRepository
from repositories.secondary_object_repository import SecondaryObjectRepository

class AttributeRootRepository(
    SecondaryObjectRepository,
    PrivacyBaseRepository,
):
    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_handle_referents(self, attr: AttributeRoot) -> List[Any]:
        return attr.get_handle_referents()

    def get_note_child_list(self, attr: AttributeRoot) -> List[Any]:
        return attr.get_note_child_list()

    def get_referenced_handles(self, attr: AttributeRoot) -> List[Tuple[str, str]]:
        return attr.get_referenced_handles()

    def get_text_data_child_list(self, attr: AttributeRoot) -> List[Any]:
        return attr.get_text_data_child_list()

    def get_text_data_list(self, attr: AttributeRoot) -> Sequence[Optional[str]]:
        return attr.get_text_data_list()

    def get_type(self, attr: AttributeRoot) -> Any:
        return attr.get_type()

    def set_type(self, attr: AttributeRoot, val: Any) -> None:
        attr.set_type(val)

    def get_value(self, attr: AttributeRoot) -> Optional[str]:
        return attr.get_value()

    def set_value(self, attr: AttributeRoot, val: str) -> None:
        attr.set_value(val)

    def is_equivalent(self, attr: AttributeRoot, other: AttributeRoot) -> int:
        return attr.is_equivalent(other)

    def merge(self, attr: AttributeRoot, acquisition: AttributeRoot) -> None:
        attr.merge(acquisition)

    def serialize(self, attr: AttributeRoot) -> Sequence[Any]:
        return attr.serialize()

    def unserialize(self, attr: AttributeRoot, data: Sequence[Any]) -> None:
        attr.unserialize(tuple(data))
