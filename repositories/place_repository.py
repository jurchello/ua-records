from __future__ import annotations

from typing import Any, Iterator, List, Optional, Tuple

from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Place

from repositories.base_repository import BaseRepository


class PlaceRepository(BaseRepository):
    """Repository for Place objects with full CRUD operations and all Place-specific methods."""

    # CRUD Operations
    def get_by_handle(self, handle: str) -> Optional[Place]:
        """Get Place by handle from database."""
        return self.db.get_place_from_handle(handle)

    def add(self, place: Place, description: str = "Add place") -> str:
        """Add new Place to database."""
        with DbTxn(description, self.db) as trans:
            return self.db.add_place(place, trans)

    def commit(self, place: Place, description: str = "Update place") -> None:
        """Commit Place changes to database."""
        with DbTxn(description, self.db) as trans:
            self.db.commit_place(place, trans)

    def iter_all(self) -> Iterator[Place]:
        """Iterate over all Places in database."""
        return self.db.iter_places()

    # Place-specific methods from stub
    def add_alternate_locations(self, place: Place, location: Any) -> None:
        """Add a Location instance to the list of alternate locations."""
        place.add_alternate_locations(location)

    def add_alternative_name(self, place: Place, name: str) -> None:
        """Add an alternative name to the place."""
        place.add_alternative_name(name)

    def add_placeref(self, place: Place, placeref: Any) -> None:
        """Add a PlaceRef instance to the list of place references."""
        place.add_placeref(placeref)

    def get_all_names(self, place: Place) -> List[Any]:
        """Return all names associated with this place."""
        return place.get_all_names()

    def get_alternate_locations(self, place: Place) -> List[Any]:
        """Return the list of alternate Location instances."""
        return place.get_alternate_locations()

    def get_alternative_names(self, place: Place) -> List[Any]:
        """Return the list of alternative names."""
        return place.get_alternative_names()

    def get_citation_child_list(self, place: Place) -> List[Any]:
        """Return the list of child secondary objects that may refer citations."""
        return place.get_citation_child_list()

    def get_code(self, place: Place) -> str:
        """Return the code of the Place."""
        return place.get_code()

    def get_handle_referents(self, place: Place) -> List[Any]:
        """Return the list of child objects which may reference primary objects."""
        return place.get_handle_referents()

    def get_latitude(self, place: Place) -> str:
        """Return the latitude of the Place."""
        return place.get_latitude()

    def get_longitude(self, place: Place) -> str:
        """Return the longitude of the Place."""
        return place.get_longitude()

    def get_name(self, place: Place) -> Any:
        """Return the name of the Place."""
        return place.get_name()

    def get_note_child_list(self, place: Place) -> List[Any]:
        """Return the list of child secondary objects that may refer notes."""
        return place.get_note_child_list()

    def get_placeref_list(self, place: Place) -> List[Any]:
        """Return the list of place references."""
        return place.get_placeref_list()

    def get_referenced_handles(self, place: Place) -> List[Tuple[str, str]]:
        """Return the list of (classname, handle) tuples for all directly referenced primary objects."""
        return place.get_referenced_handles()

    def get_text_data_child_list(self, place: Place) -> List[Any]:
        """Return the list of child objects that may carry textual data."""
        return place.get_text_data_child_list()

    def get_text_data_list(self, place: Place) -> List[str]:
        """Return the list of all textual attributes of the object."""
        return place.get_text_data_list()

    def get_title(self, place: Place) -> str:
        """Return the title of the Place."""
        return place.get_title()

    def get_type(self, place: Place) -> Any:
        """Return the type of the Place."""
        return place.get_type()

    def merge(self, place: Place, acquisition: Place) -> None:
        """Merge the content of acquisition into this place."""
        place.merge(acquisition)

    def serialize(self, place: Place) -> Tuple[Any, ...]:
        """Convert the data held in the Place to a Python tuple."""
        return place.serialize()

    def set_alternate_locations(self, place: Place, location_list: List[Any]) -> None:
        """Replace the list of alternate locations with the specified list."""
        place.set_alternate_locations(location_list)

    def set_alternative_names(self, place: Place, name_list: List[Any]) -> None:
        """Replace the list of alternative names with the specified list."""
        place.set_alternative_names(name_list)

    def set_code(self, place: Place, code: str) -> None:
        """Set the code of the Place."""
        place.set_code(code)

    def set_latitude(self, place: Place, latitude: str) -> None:
        """Set the latitude of the Place."""
        place.set_latitude(latitude)

    def set_longitude(self, place: Place, longitude: str) -> None:
        """Set the longitude of the Place."""
        place.set_longitude(longitude)

    def set_name(self, place: Place, name: Any) -> None:
        """Set the name of the Place."""
        place.set_name(name)

    def set_placeref_list(self, place: Place, placeref_list: List[Any]) -> None:
        """Set the list of place references."""
        place.set_placeref_list(placeref_list)

    def set_title(self, place: Place, title: str) -> None:
        """Set the title of the Place."""
        place.set_title(title)

    def set_type(self, place: Place, place_type: Any) -> None:
        """Set the type of the Place."""
        place.set_type(place_type)

    def unserialize(self, place: Place, data: Tuple[Any, ...]) -> None:
        """Convert the data held in a tuple back into the data in a Place object."""
        place.unserialize(data)
