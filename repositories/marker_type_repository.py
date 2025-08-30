from __future__ import annotations

from gramps.gen.lib import MarkerType

from repositories.base_repository import BaseRepository


class MarkerTypeRepository(BaseRepository):
    """Repository for MarkerType objects with all MarkerType-specific methods."""

    # MarkerType inherits from GrampsType, so it has all GrampsType methods
    def get_custom(self, marker_type: MarkerType) -> int:
        """Return the custom type value."""
        return marker_type.get_custom()

    def get_map(self, marker_type: MarkerType) -> list[tuple[int, str, str]]:
        """Return the list of type mappings."""
        return marker_type.get_map()

    def get_menu(self, marker_type: MarkerType) -> list[str]:
        """Return the menu of type options."""
        return marker_type.get_menu()

    def is_custom(self, marker_type: MarkerType) -> bool:
        """Return True if this is a custom type."""
        return marker_type.is_custom()

    def is_default(self, marker_type: MarkerType) -> bool:
        """Return True if this is the default type."""
        return marker_type.is_default()

    def serialize(self, marker_type: MarkerType) -> tuple[int, str]:
        """Convert the data held in the MarkerType to a Python tuple."""
        return marker_type.serialize()

    def set(self, marker_type: MarkerType, value: int | str) -> None:
        """Set the type value."""
        marker_type.set(value)

    def unserialize(self, marker_type: MarkerType, data: tuple[int, str]) -> None:
        """Convert the data held in a tuple back into the data in a MarkerType object."""
        marker_type.unserialize(data)
