from __future__ import annotations
from typing import Iterator, Optional, List, Any, Tuple
from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Tag

from repositories.base_repository import BaseRepository


class TagRepository(BaseRepository):
    """Repository for Tag objects with full CRUD operations and all Tag-specific methods."""

    # CRUD Operations
    def get_by_handle(self, handle: str) -> Optional[Tag]:
        """Get Tag by handle from database."""
        return self.db.get_tag_from_handle(handle)

    def add(self, tag: Tag, description: str = "Add tag") -> str:
        """Add new Tag to database."""
        with DbTxn(description, self.db) as trans:
            return self.db.add_tag(tag, trans)

    def commit(self, tag: Tag, description: str = "Update tag") -> None:
        """Commit Tag changes to database."""
        with DbTxn(description, self.db) as trans:
            self.db.commit_tag(tag, trans)

    def iter_all(self) -> Iterator[Tag]:
        """Iterate over all Tags in database."""
        return self.db.iter_tags()

    # Tag-specific methods from stub
    def are_equal(self, tag: Tag, other: Tag) -> bool:
        """Compare two Tag objects for equality."""
        return tag.are_equal(other)

    def get_color(self, tag: Tag) -> str:
        """Return the color of the Tag."""
        return tag.get_color()

    def get_name(self, tag: Tag) -> str:
        """Return the name of the Tag."""
        return tag.get_name()

    def get_priority(self, tag: Tag) -> int:
        """Return the priority of the Tag."""
        return tag.get_priority()

    def get_text_data_list(self, tag: Tag) -> List[str]:
        """Return the list of all textual attributes of the object."""
        return tag.get_text_data_list()

    def is_empty(self, tag: Tag) -> bool:
        """Return True if the Tag is empty."""
        return tag.is_empty()

    def serialize(self, tag: Tag) -> Tuple[Any, ...]:
        """Convert the data held in the Tag to a Python tuple."""
        return tag.serialize()

    def set_color(self, tag: Tag, color: str) -> None:
        """Set the color of the Tag."""
        tag.set_color(color)

    def set_name(self, tag: Tag, name: str) -> None:
        """Set the name of the Tag."""
        tag.set_name(name)

    def set_priority(self, tag: Tag, priority: int) -> None:
        """Set the priority of the Tag."""
        tag.set_priority(priority)

    def unserialize(self, tag: Tag, data: Tuple[Any, ...]) -> None:
        """Convert the data held in a tuple back into the data in a Tag object."""
        tag.unserialize(data)