from __future__ import annotations

from gramps.gen.lib import EventRoleType

from repositories.base_repository import BaseRepository


class EventRoleTypeRepository(BaseRepository):
    """Repository for EventRoleType objects with all EventRoleType-specific methods."""

    # EventRoleType inherits from GrampsType, so it has all GrampsType methods
    def get_custom(self, event_role_type: EventRoleType) -> int:
        """Return the custom type value."""
        return event_role_type.get_custom()

    def get_map(self, event_role_type: EventRoleType) -> list[tuple[int, str, str]]:
        """Return the list of type mappings."""
        return event_role_type.get_map()

    def get_menu(self, event_role_type: EventRoleType) -> list[str]:
        """Return the menu of type options."""
        return event_role_type.get_menu()

    def is_custom(self, event_role_type: EventRoleType) -> bool:
        """Return True if this is a custom type."""
        return event_role_type.is_custom()

    def is_default(self, event_role_type: EventRoleType) -> bool:
        """Return True if this is the default type."""
        return event_role_type.is_default()

    def serialize(self, event_role_type: EventRoleType) -> tuple[int, str]:
        """Convert the data held in the EventRoleType to a Python tuple."""
        return event_role_type.serialize()

    def set(self, event_role_type: EventRoleType, value: int | str) -> None:
        """Set the type value."""
        event_role_type.set(value)

    def unserialize(self, event_role_type: EventRoleType, data: tuple[int, str]) -> None:
        """Convert the data held in a tuple back into the data in an EventRoleType object."""
        event_role_type.unserialize(data)
