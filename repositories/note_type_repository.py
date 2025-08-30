from __future__ import annotations

from gramps.gen.lib import NoteType

from repositories.base_repository import BaseRepository


class NoteTypeRepository(BaseRepository):
    """Repository for NoteType objects with all NoteType-specific methods."""

    # NoteType inherits from GrampsType, so it has all GrampsType methods
    def get_custom(self, note_type: NoteType) -> int:
        """Return the custom type value."""
        return note_type.get_custom()

    def get_map(self, note_type: NoteType) -> list[tuple[int, str, str]]:
        """Return the list of type mappings."""
        return note_type.get_map()

    def get_menu(self, note_type: NoteType) -> list[str]:
        """Return the menu of type options."""
        return note_type.get_menu()

    def is_custom(self, note_type: NoteType) -> bool:
        """Return True if this is a custom type."""
        return note_type.is_custom()

    def is_default(self, note_type: NoteType) -> bool:
        """Return True if this is the default type."""
        return note_type.is_default()

    def serialize(self, note_type: NoteType) -> tuple[int, str]:
        """Convert the data held in the NoteType to a Python tuple."""
        return note_type.serialize()

    def set(self, note_type: NoteType, value: int | str) -> None:
        """Set the type value."""
        note_type.set(value)

    def unserialize(self, note_type: NoteType, data: tuple[int, str]) -> None:
        """Convert the data held in a tuple back into the data in a NoteType object."""
        note_type.unserialize(data)
