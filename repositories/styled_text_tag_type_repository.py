from __future__ import annotations
from gramps.gen.lib import StyledTextTagType

from repositories.base_repository import BaseRepository


class StyledTextTagTypeRepository(BaseRepository):
    """Repository for StyledTextTagType objects with all StyledTextTagType-specific methods."""

    # StyledTextTagType inherits from GrampsType, so it has all GrampsType methods
    def get_custom(self, styled_text_tag_type: StyledTextTagType) -> int:
        """Return the custom type value."""
        return styled_text_tag_type.get_custom()

    def get_map(self, styled_text_tag_type: StyledTextTagType) -> list[tuple[int, str, str]]:
        """Return the list of type mappings."""
        return styled_text_tag_type.get_map()

    def get_menu(self, styled_text_tag_type: StyledTextTagType) -> list[str]:
        """Return the menu of type options."""
        return styled_text_tag_type.get_menu()

    def is_custom(self, styled_text_tag_type: StyledTextTagType) -> bool:
        """Return True if this is a custom type."""
        return styled_text_tag_type.is_custom()

    def is_default(self, styled_text_tag_type: StyledTextTagType) -> bool:
        """Return True if this is the default type."""
        return styled_text_tag_type.is_default()

    def serialize(self, styled_text_tag_type: StyledTextTagType) -> tuple[int, str]:
        """Convert the data held in the StyledTextTagType to a Python tuple."""
        return styled_text_tag_type.serialize()

    def set(self, styled_text_tag_type: StyledTextTagType, value: int | str) -> None:
        """Set the type value."""
        styled_text_tag_type.set(value)

    def unserialize(self, styled_text_tag_type: StyledTextTagType, data: tuple[int, str]) -> None:
        """Convert the data held in a tuple back into the data in a StyledTextTagType object."""
        styled_text_tag_type.unserialize(data)