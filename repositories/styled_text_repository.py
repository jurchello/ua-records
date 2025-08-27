from __future__ import annotations
from typing import List, Tuple
from gramps.gen.lib import StyledText

from repositories.base_repository import BaseRepository


class StyledTextRepository(BaseRepository):
    """Repository for StyledText objects with all StyledText-specific methods."""

    # StyledText-specific methods from stub
    def get_tags(self, styled_text: StyledText) -> List[Any]:
        """Return the list of StyledTextTag objects."""
        return styled_text.get_tags()

    def serialize(self, styled_text: StyledText) -> Tuple[str, Tuple[Any, ...]]:
        """Convert the data held in the StyledText to a Python tuple."""
        return styled_text.serialize()

    def set_tags(self, styled_text: StyledText, tags: List[Any]) -> None:
        """Set the list of StyledTextTag objects."""
        styled_text.set_tags(tags)

    def unserialize(self, styled_text: StyledText, data: Tuple[str, Tuple[Any, ...]]) -> None:
        """Convert the data held in a tuple back into the data in a StyledText object."""
        styled_text.unserialize(data)