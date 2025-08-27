from __future__ import annotations
from gramps.gen.lib import SourceMediaType

from repositories.base_repository import BaseRepository


class SourceMediaTypeRepository(BaseRepository):
    """Repository for SourceMediaType objects with all SourceMediaType-specific methods."""

    # SourceMediaType inherits from GrampsType, so it has all GrampsType methods
    def get_custom(self, source_media_type: SourceMediaType) -> int:
        """Return the custom type value."""
        return source_media_type.get_custom()

    def get_map(self, source_media_type: SourceMediaType) -> list[tuple[int, str, str]]:
        """Return the list of type mappings."""
        return source_media_type.get_map()

    def get_menu(self, source_media_type: SourceMediaType) -> list[str]:
        """Return the menu of type options."""
        return source_media_type.get_menu()

    def is_custom(self, source_media_type: SourceMediaType) -> bool:
        """Return True if this is a custom type."""
        return source_media_type.is_custom()

    def is_default(self, source_media_type: SourceMediaType) -> bool:
        """Return True if this is the default type."""
        return source_media_type.is_default()

    def serialize(self, source_media_type: SourceMediaType) -> tuple[int, str]:
        """Convert the data held in the SourceMediaType to a Python tuple."""
        return source_media_type.serialize()

    def set(self, source_media_type: SourceMediaType, value: int | str) -> None:
        """Set the type value."""
        source_media_type.set(value)

    def unserialize(self, source_media_type: SourceMediaType, data: tuple[int, str]) -> None:
        """Convert the data held in a tuple back into the data in a SourceMediaType object."""
        source_media_type.unserialize(data)