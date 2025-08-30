# pylint: disable=duplicate-code
from __future__ import annotations

from gramps.gen.lib import NameType

from repositories.base_repository import BaseRepository


class NameTypeRepository(BaseRepository):
    """Repository for NameType objects with all NameType-specific methods."""

    # NameType inherits from GrampsType, so it has all GrampsType methods
    def get_custom(self, name_type: NameType) -> int:
        """Return the custom type value."""
        return name_type.get_custom()

    def get_map(self, name_type: NameType) -> list[tuple[int, str, str]]:
        """Return the list of type mappings."""
        return name_type.get_map()

    def get_menu(self, name_type: NameType) -> list[str]:
        """Return the menu of type options."""
        return name_type.get_menu()

    def is_custom(self, name_type: NameType) -> bool:
        """Return True if this is a custom type."""
        return name_type.is_custom()

    def is_default(self, name_type: NameType) -> bool:
        """Return True if this is the default type."""
        return name_type.is_default()

    def serialize(self, name_type: NameType) -> tuple[int, str]:
        """Convert the data held in the NameType to a Python tuple."""
        return name_type.serialize()

    def set(self, name_type: NameType, value: int | str) -> None:
        """Set the type value."""
        name_type.set(value)

    def unserialize(self, name_type: NameType, data: tuple[int, str]) -> None:
        """Convert the data held in a tuple back into the data in a NameType object."""
        name_type.unserialize(data)
