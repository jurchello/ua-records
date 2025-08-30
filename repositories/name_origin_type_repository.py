from __future__ import annotations

from gramps.gen.lib import NameOriginType

from repositories.base_repository import BaseRepository


class NameOriginTypeRepository(BaseRepository):
    """Repository for NameOriginType objects with all NameOriginType-specific methods."""

    # NameOriginType inherits from GrampsType, so it has all GrampsType methods
    def get_custom(self, name_origin_type: NameOriginType) -> int:
        """Return the custom type value."""
        return name_origin_type.get_custom()

    def get_map(self, name_origin_type: NameOriginType) -> list[tuple[int, str, str]]:
        """Return the list of type mappings."""
        return name_origin_type.get_map()

    def get_menu(self, name_origin_type: NameOriginType) -> list[str]:
        """Return the menu of type options."""
        return name_origin_type.get_menu()

    def is_custom(self, name_origin_type: NameOriginType) -> bool:
        """Return True if this is a custom type."""
        return name_origin_type.is_custom()

    def is_default(self, name_origin_type: NameOriginType) -> bool:
        """Return True if this is the default type."""
        return name_origin_type.is_default()

    def serialize(self, name_origin_type: NameOriginType) -> tuple[int, str]:
        """Convert the data held in the NameOriginType to a Python tuple."""
        return name_origin_type.serialize()

    def set(self, name_origin_type: NameOriginType, value: int | str) -> None:
        """Set the type value."""
        name_origin_type.set(value)

    def unserialize(self, name_origin_type: NameOriginType, data: tuple[int, str]) -> None:
        """Convert the data held in a tuple back into the data in a NameOriginType object."""
        name_origin_type.unserialize(data)
