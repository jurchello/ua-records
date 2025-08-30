from __future__ import annotations

from typing import Any, List, Tuple

from gramps.gen.lib.attrbase import SrcAttributeBase

from repositories.base_repository import BaseRepository


class SrcAttributeBaseRepository(BaseRepository):
    """Repository for SrcAttributeBase objects with all SrcAttributeBase-specific methods."""

    # SrcAttributeBase-specific methods from stub
    def add_attribute(self, src_attr_base: SrcAttributeBase, attribute: Any) -> None:
        """Add the Attribute instance to the list of source attributes."""
        src_attr_base.add_attribute(attribute)

    def get_attribute_list(self, src_attr_base: SrcAttributeBase) -> List[Any]:
        """Return the list of source Attribute instances."""
        return src_attr_base.get_attribute_list()

    def remove_attribute(self, src_attr_base: SrcAttributeBase, attribute: Any) -> bool:
        """Remove the specified Attribute from the source attribute list."""
        return src_attr_base.remove_attribute(attribute)

    def serialize(self, src_attr_base: SrcAttributeBase) -> Tuple[Any, ...]:
        """Convert the data held in the SrcAttributeBase to a Python tuple."""
        return src_attr_base.serialize()

    def set_attribute_list(self, src_attr_base: SrcAttributeBase, attribute_list: List[Any]) -> None:
        """Assign the passed list to the source attribute list."""
        src_attr_base.set_attribute_list(attribute_list)

    def unserialize(self, src_attr_base: SrcAttributeBase, data: Tuple[Any, ...]) -> None:
        """Convert the data held in a tuple back into the data in a SrcAttributeBase object."""
        src_attr_base.unserialize(data)
