from __future__ import annotations
from typing import List, Any, Tuple
from gramps.gen.lib import PrimaryObject

from repositories.base_repository import BaseRepository


class PrimaryObjectRepository(BaseRepository):
    """Repository for PrimaryObject objects with all PrimaryObject-specific methods."""

    # PrimaryObject-specific methods from stub
    def has_handle_reference(self, primary_obj: PrimaryObject, classname: str, handle: str) -> bool:
        """Return True if the object has a reference to the given primary object."""
        return primary_obj.has_handle_reference(classname, handle)

    def remove_handle_references(self, primary_obj: PrimaryObject, classname: str, handle_list: List[str]) -> None:
        """Remove all references to the handles in the list."""
        primary_obj.remove_handle_references(classname, handle_list)

    def replace_handle_reference(self, primary_obj: PrimaryObject, classname: str, old_handle: str, new_handle: str) -> None:
        """Replace all references to old_handle with new_handle."""
        primary_obj.replace_handle_reference(classname, old_handle, new_handle)