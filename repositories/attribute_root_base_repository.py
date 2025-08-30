from __future__ import annotations

from typing import Any, List, Tuple

from gramps.gen.lib.attrbase import AttributeRootBase

from repositories.base_repository import BaseRepository


class AttributeRootBaseRepository(BaseRepository):
    """Repository for AttributeRootBase objects with all AttributeRootBase-specific methods."""

    # AttributeRootBase-specific methods from stub
    def add_attribute(self, attr_root_base: AttributeRootBase, attribute: Any) -> None:
        """Add the Attribute instance to the list of attributes."""
        attr_root_base.add_attribute(attribute)

    def get_attribute_list(self, attr_root_base: AttributeRootBase) -> List[Any]:
        """Return the list of Attribute instances."""
        return attr_root_base.get_attribute_list()

    def remove_attribute(self, attr_root_base: AttributeRootBase, attribute: Any) -> bool:
        """Remove the specified Attribute from the attribute list."""
        return attr_root_base.remove_attribute(attribute)

    def serialize(self, attr_root_base: AttributeRootBase) -> Tuple[Any, ...]:
        """Convert the data held in the AttributeRootBase to a Python tuple."""
        return attr_root_base.serialize()

    def set_attribute_list(self, attr_root_base: AttributeRootBase, attribute_list: List[Any]) -> None:
        """Assign the passed list to the attribute list."""
        attr_root_base.set_attribute_list(attribute_list)

    def unserialize(self, attr_root_base: AttributeRootBase, data: Tuple[Any, ...]) -> None:
        """Convert the data held in a tuple back into the data in an AttributeRootBase object."""
        attr_root_base.unserialize(data)
