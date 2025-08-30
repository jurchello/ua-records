from __future__ import annotations

from gramps.gen.lib import EventType

from repositories.base_repository import BaseRepository


class EventTypeRepository(BaseRepository):
    """Repository for EventType objects with all EventType-specific methods."""

    # EventType inherits from GrampsType, so it has all GrampsType methods
    def get_custom(self, event_type: EventType) -> int:
        """Return the custom type value."""
        return event_type.get_custom()

    def get_map(self, event_type: EventType) -> list[tuple[int, str, str]]:
        """Return the list of type mappings."""
        return event_type.get_map()

    def get_menu(self, event_type: EventType) -> list[str]:
        """Return the menu of type options."""
        return event_type.get_menu()

    def is_custom(self, event_type: EventType) -> bool:
        """Return True if this is a custom type."""
        return event_type.is_custom()

    def is_default(self, event_type: EventType) -> bool:
        """Return True if this is the default type."""
        return event_type.is_default()

    def serialize(self, event_type: EventType) -> tuple[int, str]:
        """Convert the data held in the EventType to a Python tuple."""
        return event_type.serialize()

    def set(self, event_type: EventType, value: int | str) -> None:
        """Set the type value."""
        event_type.set(value)

    def unserialize(self, event_type: EventType, data: tuple[int, str]) -> None:
        """Convert the data held in a tuple back into the data in an EventType object."""
        event_type.unserialize(data)
