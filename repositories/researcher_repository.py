from __future__ import annotations
from typing import Tuple, Any
from gramps.gen.lib import Researcher

from repositories.base_repository import BaseRepository


class ResearcherRepository(BaseRepository):
    """Repository for Researcher objects with all Researcher-specific methods."""

    # Researcher-specific methods from stub
    def get_address(self, researcher: Researcher) -> str:
        """Return the address of the Researcher."""
        return researcher.get_address()

    def get_email(self, researcher: Researcher) -> str:
        """Return the email address of the Researcher."""
        return researcher.get_email()

    def get_name(self, researcher: Researcher) -> str:
        """Return the name of the Researcher."""
        return researcher.get_name()

    def serialize(self, researcher: Researcher) -> Tuple[Any, ...]:
        """Convert the data held in the Researcher to a Python tuple."""
        return researcher.serialize()

    def set_address(self, researcher: Researcher, address: str) -> None:
        """Set the address of the Researcher."""
        researcher.set_address(address)

    def set_email(self, researcher: Researcher, email: str) -> None:
        """Set the email address of the Researcher."""
        researcher.set_email(email)

    def set_name(self, researcher: Researcher, name: str) -> None:
        """Set the name of the Researcher."""
        researcher.set_name(name)

    def unserialize(self, researcher: Researcher, data: Tuple[Any, ...]) -> None:
        """Convert the data held in a tuple back into the data in a Researcher object."""
        researcher.unserialize(data)