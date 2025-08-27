from __future__ import annotations
from gramps.gen.lib import ChildRefType

from repositories.base_repository import BaseRepository


class ChildRefTypeRepository(BaseRepository):
    """Repository for ChildRefType objects with all ChildRefType-specific methods."""

    # ChildRefType inherits from GrampsType, so it has all GrampsType methods
    def get_custom(self, child_ref_type: ChildRefType) -> int:
        """Return the custom type value."""
        return child_ref_type.get_custom()

    def get_map(self, child_ref_type: ChildRefType) -> list[tuple[int, str, str]]:
        """Return the list of type mappings."""
        return child_ref_type.get_map()

    def get_menu(self, child_ref_type: ChildRefType) -> list[str]:
        """Return the menu of type options."""
        return child_ref_type.get_menu()

    def is_custom(self, child_ref_type: ChildRefType) -> bool:
        """Return True if this is a custom type."""
        return child_ref_type.is_custom()

    def is_default(self, child_ref_type: ChildRefType) -> bool:
        """Return True if this is the default type."""
        return child_ref_type.is_default()

    def serialize(self, child_ref_type: ChildRefType) -> tuple[int, str]:
        """Convert the data held in the ChildRefType to a Python tuple."""
        return child_ref_type.serialize()

    def set(self, child_ref_type: ChildRefType, value: int | str) -> None:
        """Set the type value."""
        child_ref_type.set(value)

    def unserialize(self, child_ref_type: ChildRefType, data: tuple[int, str]) -> None:
        """Convert the data held in a tuple back into the data in a ChildRefType object."""
        child_ref_type.unserialize(data)