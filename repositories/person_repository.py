from __future__ import annotations

from typing import Any, Iterator, List, Optional, Tuple

from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Person

from repositories.base_repository import BaseRepository


class PersonRepository(BaseRepository):
    """Repository for Person objects with full CRUD operations and all Person-specific methods."""

    # CRUD Operations
    def get_by_handle(self, handle: str) -> Optional[Person]:
        """Get Person by handle from database."""
        return self.db.get_person_from_handle(handle)

    def add(self, person: Person, description: str = "Add person") -> str:
        """Add new Person to database."""
        with DbTxn(description, self.db) as trans:
            return self.db.add_person(person, trans)

    def commit(self, person: Person, description: str = "Update person") -> None:
        """Commit Person changes to database."""
        with DbTxn(description, self.db) as trans:
            self.db.commit_person(person, trans)

    def iter_all(self) -> Iterator[Person]:
        """Iterate over all Persons in database."""
        return self.db.iter_people()

    # Person-specific methods from stub
    def get_gender(self, person: Person) -> int:
        """Return the gender of the Person."""
        return person.get_gender()

    def set_gender(self, person: Person, gender: int) -> None:
        """Set the gender of the Person."""
        person.set_gender(gender)

    def add_alternate_name(self, person: Person, name: Any) -> None:
        """Add a Name instance to the list of alternative names."""
        person.add_alternate_name(name)

    def add_event_ref(self, person: Person, event_ref: Any) -> None:
        """Add the EventRef to the Person instance's EventRef list."""
        person.add_event_ref(event_ref)

    def add_family_handle(self, person: Person, family_handle: str) -> None:
        """Add the Family handle to the Person instance's Family list."""
        person.add_family_handle(family_handle)

    def add_parent_family_handle(self, person: Person, family_handle: str) -> None:
        """Add the Family handle to the Person instance's list of families in which it is a child."""
        person.add_parent_family_handle(family_handle)

    def add_person_ref(self, person: Person, person_ref: Any) -> None:
        """Add the PersonRef to the Person instance's PersonRef list."""
        person.add_person_ref(person_ref)

    def clear_family_handle_list(self, person: Person) -> None:
        """Remove all Family handles from the Family list."""
        person.clear_family_handle_list()

    def clear_parent_family_handle_list(self, person: Person) -> None:
        """Remove all Family handles from the parent Family list."""
        person.clear_parent_family_handle_list()

    def get_alternate_names(self, person: Person) -> List[Any]:
        """Return the list of alternate Name instances."""
        return person.get_alternate_names()

    def get_birth_ref(self, person: Person) -> Optional[Any]:
        """Return the EventRef for Person's birth event."""
        return person.get_birth_ref()

    def get_citation_child_list(self, person: Person) -> List[Any]:
        """Return the list of child secondary objects that may refer citations."""
        return person.get_citation_child_list()

    def get_death_ref(self, person: Person) -> Optional[Any]:
        """Return the EventRef for the Person's death event."""
        return person.get_death_ref()

    def get_event_ref_list(self, person: Person) -> List[Any]:
        """Return the list of EventRef objects associated with Event instances."""
        return person.get_event_ref_list()

    def get_family_handle_list(self, person: Person) -> List[str]:
        """Return the list of Family handles in which the person is a parent or spouse."""
        return person.get_family_handle_list()

    def get_handle_referents(self, person: Person) -> List[Any]:
        """Return the list of child objects which may reference primary objects."""
        return person.get_handle_referents()

    def get_main_parents_family_handle(self, person: Person) -> Optional[str]:
        """Return the handle of the Family considered to be the main Family in which the Person is a child."""
        return person.get_main_parents_family_handle()

    def get_nick_name(self, person: Person) -> Optional[str]:
        """Get the nickname of the person."""
        return person.get_nick_name()

    def get_note_child_list(self, person: Person) -> List[Any]:
        """Return the list of child secondary objects that may refer notes."""
        return person.get_note_child_list()

    def get_parent_family_handle_list(self, person: Person) -> List[str]:
        """Return the list of Family handles in which the person is a child."""
        return person.get_parent_family_handle_list()

    def get_person_ref_list(self, person: Person) -> List[Any]:
        """Return the list of PersonRef objects."""
        return person.get_person_ref_list()

    def get_primary_event_ref_list(self, person: Person) -> Any:
        """Return the list of EventRef objects associated with Event instances
        that have been marked as primary events."""
        return person.get_primary_event_ref_list()

    def get_primary_name(self, person: Person) -> Any:
        """Return the Name instance marked as the Person's primary name."""
        return person.get_primary_name()

    def get_referenced_handles(self, person: Person) -> List[Tuple[str, str]]:
        """Return the list of (classname, handle) tuples for all directly referenced primary objects."""
        return person.get_referenced_handles()

    def get_text_data_child_list(self, person: Person) -> List[Any]:
        """Return the list of child objects that may carry textual data."""
        return person.get_text_data_child_list()

    def get_text_data_list(self, person: Person) -> List[str]:
        """Return the list of all textual attributes of the object."""
        return person.get_text_data_list()

    def merge(self, person: Person, acquisition: Person) -> None:
        """Merge the content of acquisition into this person."""
        person.merge(acquisition)

    def remove_family_handle(self, person: Person, family_handle: str) -> bool:
        """Remove the specified Family handle from the list of marriages/partnerships."""
        return person.remove_family_handle(family_handle)

    def remove_parent_family_handle(self, person: Person, family_handle: str) -> Optional[Tuple[str, str, str]]:
        """Remove the specified Family handle from the list of parent families."""
        return person.remove_parent_family_handle(family_handle)

    def serialize(self, person: Person) -> Tuple[Any, ...]:
        """Convert the data held in the Person to a Python tuple that represents all the data elements."""
        return person.serialize()

    def set_alternate_names(self, person: Person, alt_name_list: List[Any]) -> None:
        """Change the list of alternate names to the passed list."""
        person.set_alternate_names(alt_name_list)

    def set_birth_ref(self, person: Person, event_ref: Any) -> None:
        """Assign the birth event to the Person object."""
        person.set_birth_ref(event_ref)

    def set_death_ref(self, person: Person, event_ref: Any) -> None:
        """Assign the death event to the Person object."""
        person.set_death_ref(event_ref)

    def set_event_ref_list(self, person: Person, event_ref_list: List[Any]) -> None:
        """Set the Person instance's EventRef list to the passed list."""
        person.set_event_ref_list(event_ref_list)

    def set_family_handle_list(self, person: Person, family_list: List[str]) -> None:
        """Assign the passed list to the Person's list of families in which it is a parent or spouse."""
        person.set_family_handle_list(family_list)

    def set_main_parent_family_handle(self, person: Person, family_handle: str) -> bool:
        """Set the main Family in which the Person is a child."""
        return person.set_main_parent_family_handle(family_handle)

    def set_parent_family_handle_list(self, person: Person, family_list: List[str]) -> None:
        """Return the list of Family handles in which the person is a child."""
        person.set_parent_family_handle_list(family_list)

    def set_person_ref_list(self, person: Person, person_ref_list: List[Any]) -> None:
        """Set the Person instance's PersonRef list to the passed list."""
        person.set_person_ref_list(person_ref_list)

    def set_preferred_family_handle(self, person: Person, family_handle: str) -> bool:
        """Set the family_handle specified to be the preferred Family."""
        return person.set_preferred_family_handle(family_handle)

    def set_primary_name(self, person: Person, name: Any) -> None:
        """Set the primary name of the Person to the specified Name instance."""
        person.set_primary_name(name)

    def unserialize(self, person: Person, data: Tuple[Any, ...]) -> None:
        """Convert the data held in a tuple created by the serialize method back into the data in a Person object."""
        person.unserialize(data)
