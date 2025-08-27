from __future__ import annotations
from gramps.gen.lib import RepositoryType

from repositories.base_repository import BaseRepository


class RepositoryTypeRepository(BaseRepository):
    """Repository for RepositoryType objects with all RepositoryType-specific methods."""

    # RepositoryType inherits from GrampsType, so it has all GrampsType methods
    def get_custom(self, repository_type: RepositoryType) -> int:
        """Return the custom type value."""
        return repository_type.get_custom()

    def get_map(self, repository_type: RepositoryType) -> list[tuple[int, str, str]]:
        """Return the list of type mappings."""
        return repository_type.get_map()

    def get_menu(self, repository_type: RepositoryType) -> list[str]:
        """Return the menu of type options."""
        return repository_type.get_menu()

    def is_custom(self, repository_type: RepositoryType) -> bool:
        """Return True if this is a custom type."""
        return repository_type.is_custom()

    def is_default(self, repository_type: RepositoryType) -> bool:
        """Return True if this is the default type."""
        return repository_type.is_default()

    def serialize(self, repository_type: RepositoryType) -> tuple[int, str]:
        """Convert the data held in the RepositoryType to a Python tuple."""
        return repository_type.serialize()

    def set(self, repository_type: RepositoryType, value: int | str) -> None:
        """Set the type value."""
        repository_type.set(value)

    def unserialize(self, repository_type: RepositoryType, data: tuple[int, str]) -> None:
        """Convert the data held in a tuple back into the data in a RepositoryType object."""
        repository_type.unserialize(data)