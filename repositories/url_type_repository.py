from __future__ import annotations
from gramps.gen.lib import UrlType

from repositories.base_repository import BaseRepository


class UrlTypeRepository(BaseRepository):
    """Repository for UrlType objects with all UrlType-specific methods."""

    # UrlType inherits from GrampsType, so it has all GrampsType methods
    def get_custom(self, url_type: UrlType) -> int:
        """Return the custom type value."""
        return url_type.get_custom()

    def get_map(self, url_type: UrlType) -> list[tuple[int, str, str]]:
        """Return the list of type mappings."""
        return url_type.get_map()

    def get_menu(self, url_type: UrlType) -> list[str]:
        """Return the menu of type options."""
        return url_type.get_menu()

    def is_custom(self, url_type: UrlType) -> bool:
        """Return True if this is a custom type."""
        return url_type.is_custom()

    def is_default(self, url_type: UrlType) -> bool:
        """Return True if this is the default type."""
        return url_type.is_default()

    def serialize(self, url_type: UrlType) -> tuple[int, str]:
        """Convert the data held in the UrlType to a Python tuple."""
        return url_type.serialize()

    def set(self, url_type: UrlType, value: int | str) -> None:
        """Set the type value."""
        url_type.set(value)

    def unserialize(self, url_type: UrlType, data: tuple[int, str]) -> None:
        """Convert the data held in a tuple back into the data in a UrlType object."""
        url_type.unserialize(data)