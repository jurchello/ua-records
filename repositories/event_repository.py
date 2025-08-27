from __future__ import annotations
from typing import Iterator, Optional, List, Any, Tuple
from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Event

from repositories.base_repository import BaseRepository


class EventRepository(BaseRepository):
    """Repository for Event objects with full CRUD operations and all Event-specific methods."""

    # CRUD Operations
    def get_by_handle(self, handle: str) -> Optional[Event]:
        """Get Event by handle from database."""
        return self.db.get_event_from_handle(handle)

    def add(self, event: Event, description: str = "Add event") -> str:
        """Add new Event to database."""
        with DbTxn(description, self.db) as trans:
            return self.db.add_event(event, trans)

    def commit(self, event: Event, description: str = "Update event") -> None:
        """Commit Event changes to database."""
        with DbTxn(description, self.db) as trans:
            self.db.commit_event(event, trans)

    def iter_all(self) -> Iterator[Event]:
        """Iterate over all Events in database."""
        return self.db.iter_events()

    # Event-specific methods from stub
    def are_equal(self, event: Event, other: Event) -> bool:
        """Compare two Event objects for equality."""
        return event.are_equal(other)

    def get_citation_child_list(self, event: Event) -> List[Any]:
        """Return the list of child secondary objects that may refer citations."""
        return event.get_citation_child_list()

    def get_description(self, event: Event) -> str:
        """Return the description of the Event."""
        return event.get_description()

    def get_handle_referents(self, event: Event) -> List[Any]:
        """Return the list of child objects which may reference primary objects."""
        return event.get_handle_referents()

    def get_note_child_list(self, event: Event) -> List[Any]:
        """Return the list of child secondary objects that may refer notes."""
        return event.get_note_child_list()

    def get_referenced_handles(self, event: Event) -> List[Tuple[str, str]]:
        """Return the list of (classname, handle) tuples for all directly referenced primary objects."""
        return event.get_referenced_handles()

    def get_text_data_child_list(self, event: Event) -> List[Any]:
        """Return the list of child objects that may carry textual data."""
        return event.get_text_data_child_list()

    def get_text_data_list(self, event: Event) -> List[str]:
        """Return the list of all textual attributes of the object."""
        return event.get_text_data_list()

    def get_type(self, event: Event) -> Tuple[int, str]:
        """Return the type of the Event."""
        return event.get_type()

    def is_empty(self, event: Event) -> bool:
        """Return True if the Event is empty."""
        return event.is_empty()

    def merge(self, event: Event, acquisition: Event) -> None:
        """Merge the content of acquisition into this event."""
        event.merge(acquisition)

    def serialize(self, event: Event, no_text_date: bool = False) -> Tuple[Any, ...]:
        """Convert the data held in the Event to a Python tuple."""
        return event.serialize(no_text_date)

    def set_description(self, event: Event, description: str) -> None:
        """Set the description of the Event."""
        event.set_description(description)

    def set_type(self, event: Event, the_type: Tuple[int, str]) -> None:
        """Set the type of the Event."""
        event.set_type(the_type)

    def unserialize(self, event: Event, data: Tuple[Any, ...]) -> None:
        """Convert the data held in a tuple back into the data in an Event object."""
        event.unserialize(data)