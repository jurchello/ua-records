from __future__ import annotations
from gramps.gen.lib import FamilyRelType

from repositories.base_repository import BaseRepository


class FamilyRelTypeRepository(BaseRepository):
    """Repository for FamilyRelType objects with all FamilyRelType-specific methods."""

    # FamilyRelType inherits from GrampsType, so it has all GrampsType methods
    def get_custom(self, family_rel_type: FamilyRelType) -> int:
        """Return the custom type value."""
        return family_rel_type.get_custom()

    def get_map(self, family_rel_type: FamilyRelType) -> list[tuple[int, str, str]]:
        """Return the list of type mappings."""
        return family_rel_type.get_map()

    def get_menu(self, family_rel_type: FamilyRelType) -> list[str]:
        """Return the menu of type options."""
        return family_rel_type.get_menu()

    def is_custom(self, family_rel_type: FamilyRelType) -> bool:
        """Return True if this is a custom type."""
        return family_rel_type.is_custom()

    def is_default(self, family_rel_type: FamilyRelType) -> bool:
        """Return True if this is the default type."""
        return family_rel_type.is_default()

    def serialize(self, family_rel_type: FamilyRelType) -> tuple[int, str]:
        """Convert the data held in the FamilyRelType to a Python tuple."""
        return family_rel_type.serialize()

    def set(self, family_rel_type: FamilyRelType, value: int | str) -> None:
        """Set the type value."""
        family_rel_type.set(value)

    def unserialize(self, family_rel_type: FamilyRelType, data: tuple[int, str]) -> None:
        """Convert the data held in a tuple back into the data in a FamilyRelType object."""
        family_rel_type.unserialize(data)