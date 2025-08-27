from __future__ import annotations
from gramps.gen.lib import PlaceType

from repositories.base_repository import BaseRepository


class PlaceTypeRepository(BaseRepository):
    """Repository for PlaceType objects with all PlaceType-specific methods."""

    # PlaceType inherits from GrampsType, so it has all GrampsType methods
    def get_custom(self, place_type: PlaceType) -> int:
        """Return the custom type value."""
        return place_type.get_custom()

    def get_map(self, place_type: PlaceType) -> list[tuple[int, str, str]]:
        """Return the list of type mappings."""
        return place_type.get_map()

    def get_menu(self, place_type: PlaceType) -> list[str]:
        """Return the menu of type options."""
        return place_type.get_menu()

    def is_custom(self, place_type: PlaceType) -> bool:
        """Return True if this is a custom type."""
        return place_type.is_custom()

    def is_default(self, place_type: PlaceType) -> bool:
        """Return True if this is the default type."""
        return place_type.is_default()

    def serialize(self, place_type: PlaceType) -> tuple[int, str]:
        """Convert the data held in the PlaceType to a Python tuple."""
        return place_type.serialize()

    def set(self, place_type: PlaceType, value: int | str) -> None:
        """Set the type value."""
        place_type.set(value)

    def unserialize(self, place_type: PlaceType, data: tuple[int, str]) -> None:
        """Convert the data held in a tuple back into the data in a PlaceType object."""
        place_type.unserialize(data)