from __future__ import annotations

from typing import Any, List, Tuple

from gramps.gen.lib.attrbase import AttributeRootBase

from repositories.repository_core import RepositoryCore


class AttributeRootBaseRepository(RepositoryCore):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def add_attribute(self, attr_root_base: AttributeRootBase, attribute: Any) -> None:
        attr_root_base.add_attribute(attribute)

    def get_attribute_list(self, attr_root_base: AttributeRootBase) -> List[Any]:
        return attr_root_base.get_attribute_list()

    def remove_attribute(self, attr_root_base: AttributeRootBase, attribute: Any) -> bool:
        return attr_root_base.remove_attribute(attribute)

    def serialize(self, attr_root_base: AttributeRootBase) -> List[Any]:
        return attr_root_base.serialize()

    def set_attribute_list(self, attr_root_base: AttributeRootBase, attribute_list: List[Any]) -> None:
        attr_root_base.set_attribute_list(attribute_list)

    def unserialize(self, attr_root_base: AttributeRootBase, data: Tuple[Any, ...]) -> None:
        attr_root_base.unserialize(data)
