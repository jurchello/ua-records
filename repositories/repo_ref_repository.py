from __future__ import annotations

from typing import Any, List, Tuple

from gramps.gen.lib import RepoRef

from repositories.base_repository import BaseRepository


class RepoRefRepository(BaseRepository):
    """Repository for RepoRef objects with all RepoRef-specific methods."""

    # RepoRef-specific methods from stub
    def get_handle_referents(self, reporef: RepoRef) -> List[Any]:
        """Return the list of child objects which may reference primary objects."""
        return reporef.get_handle_referents()

    def get_media_type(self, reporef: RepoRef) -> Tuple[int, str]:
        """Return the media type of the RepoRef."""
        return reporef.get_media_type()

    def get_note_child_list(self, reporef: RepoRef) -> List[Any]:
        """Return the list of child secondary objects that may refer notes."""
        return reporef.get_note_child_list()

    def get_referenced_handles(self, reporef: RepoRef) -> List[Tuple[str, str]]:
        """Return the list of (classname, handle) tuples for all directly referenced primary objects."""
        return reporef.get_referenced_handles()

    def get_text_data_child_list(self, reporef: RepoRef) -> List[Any]:
        """Return the list of child objects that may carry textual data."""
        return reporef.get_text_data_child_list()

    def get_text_data_list(self, reporef: RepoRef) -> List[str]:
        """Return the list of all textual attributes of the object."""
        return reporef.get_text_data_list()

    def is_equivalent(self, reporef: RepoRef, other: RepoRef) -> bool:
        """Compare two RepoRef objects for equivalence."""
        return reporef.is_equivalent(other)

    def merge(self, reporef: RepoRef, acquisition: RepoRef) -> None:
        """Merge the content of acquisition into this reporef."""
        reporef.merge(acquisition)

    def serialize(self, reporef: RepoRef) -> Tuple[Any, ...]:
        """Convert the data held in the RepoRef to a Python tuple."""
        return reporef.serialize()

    def set_media_type(self, reporef: RepoRef, media_type: Tuple[int, str]) -> None:
        """Set the media type of the RepoRef."""
        reporef.set_media_type(media_type)

    def unserialize(self, reporef: RepoRef, data: Tuple[Any, ...]) -> None:
        """Convert the data held in a tuple back into the data in a RepoRef object."""
        reporef.unserialize(data)
