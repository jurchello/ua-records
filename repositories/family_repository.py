from __future__ import annotations

from typing import Any, Iterator, List, Optional, Tuple

from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Family
from gramps.gen.lib.childref import ChildRef
from gramps.gen.lib.eventref import EventRef
from gramps.gen.lib.primaryobj import PrimaryObject

from repositories.base_repository import BaseRepository


class FamilyRepository(BaseRepository):
    """Repository for Family objects with full CRUD operations and all Family-specific methods."""

    # CRUD Operations
    def get_by_handle(self, handle: str) -> Optional[Family]:
        """Get Family by handle from database."""
        return self.db.get_family_from_handle(handle)

    def add(self, family: Family, description: str = "Add family") -> str:
        """Add new Family to database."""
        with DbTxn(description, self.db) as trans:
            return self.db.add_family(family, trans)

    def commit(self, family: Family, description: str = "Update family") -> None:
        """Commit Family changes to database."""
        with DbTxn(description, self.db) as trans:
            self.db.commit_family(family, trans)

    def iter_all(self) -> Iterator[Family]:
        """Iterate over all Families in database."""
        return self.db.iter_families()

    # Family-specific methods from stub
    def add_child_ref(self, family: Family, child_ref: ChildRef) -> None:
        """Add a ChildRef to the family."""
        family.add_child_ref(child_ref)

    def add_event_ref(self, family: Family, event_ref: EventRef) -> None:
        """Add an EventRef to the family."""
        family.add_event_ref(event_ref)

    def get_child_ref_list(self, family: Family) -> List[ChildRef]:
        """Return the list of ChildRef objects."""
        return family.get_child_ref_list()

    def get_citation_child_list(self, family: Family) -> List[Any]:
        """Return the list of child secondary objects that may refer citations."""
        return family.get_citation_child_list()

    def get_event_list(self, family: Family) -> List[Any]:
        """Return the list of event objects."""
        return family.get_event_list()

    def get_event_ref_list(self, family: Family) -> List[EventRef]:
        """Return the list of EventRef objects."""
        return family.get_event_ref_list()

    def get_father_handle(self, family: Family) -> str:
        """Return the handle of the father."""
        return family.get_father_handle()

    def get_handle_referents(self, family: Family) -> List[Any]:
        """Return the list of child objects which may reference primary objects."""
        return family.get_handle_referents()

    def get_mother_handle(self, family: Family) -> str:
        """Return the handle of the mother."""
        return family.get_mother_handle()

    def get_note_child_list(self, family: Family) -> List[Any]:
        """Return the list of child secondary objects that may refer notes."""
        return family.get_note_child_list()

    def get_referenced_handles(self, family: Family) -> List[Tuple[str, str]]:
        """Return the list of (classname, handle) tuples for all directly referenced primary objects."""
        return family.get_referenced_handles()

    def get_relationship(self, family: Family) -> Tuple[int, str]:
        """Return the relationship type tuple."""
        return family.get_relationship()

    def get_text_data_child_list(self, family: Family) -> List[Any]:
        """Return the list of child objects that may carry textual data."""
        return family.get_text_data_child_list()

    def get_text_data_list(self, family: Family) -> List[str]:
        """Return the list of all textual attributes of the object."""
        return family.get_text_data_list()

    def merge(self, family: Family, acquisition: PrimaryObject) -> None:
        """Merge the content of acquisition into this family."""
        family.merge(acquisition)

    def remove_child_handle(self, family: Family, child_handle: str) -> bool:
        """Remove the specified child handle from the family."""
        return family.remove_child_handle(child_handle)

    def remove_child_ref(self, family: Family, child_ref: ChildRef) -> bool:
        """Remove the specified ChildRef from the family."""
        return family.remove_child_ref(child_ref)

    def serialize(self, family: Family) -> Tuple[Any, ...]:
        """Convert the data held in the Family to a Python tuple that represents all the data elements."""
        return family.serialize()

    def set_child_ref_list(self, family: Family, child_ref_list: List[ChildRef]) -> None:
        """Set the Family instance's ChildRef list to the passed list."""
        family.set_child_ref_list(child_ref_list)

    def set_event_ref_list(self, family: Family, event_ref_list: List[EventRef]) -> None:
        """Set the Family instance's EventRef list to the passed list."""
        family.set_event_ref_list(event_ref_list)

    def set_father_handle(self, family: Family, person_handle: str) -> None:
        """Set the father handle for the family."""
        family.set_father_handle(person_handle)

    def set_mother_handle(self, family: Family, person_handle: str) -> None:
        """Set the mother handle for the family."""
        family.set_mother_handle(person_handle)

    def set_relationship(self, family: Family, relationship_type: Tuple[int, str]) -> None:
        """Set the relationship type for the family."""
        family.set_relationship(relationship_type)

    def unserialize(self, family: Family, data: Tuple[Any, ...]) -> None:
        """Convert the data held in a tuple created by the serialize method back into the data in a Family object."""
        family.unserialize(data)
