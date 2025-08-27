from __future__ import annotations
from typing import List, Tuple
from gramps.gen.lib import StyledTextTag

from repositories.base_repository import BaseRepository


class StyledTextTagRepository(BaseRepository):
    """Repository for StyledTextTag objects with all StyledTextTag-specific methods."""

    # StyledTextTag-specific methods from stub
    def get_name(self, tag: StyledTextTag) -> Any:
        """Return the name of the StyledTextTag."""
        return tag.get_name()

    def get_ranges(self, tag: StyledTextTag) -> List[Tuple[int, int]]:
        """Return the list of ranges."""
        return tag.get_ranges()

    def get_value(self, tag: StyledTextTag) -> str:
        """Return the value of the StyledTextTag."""
        return tag.get_value()

    def serialize(self, tag: StyledTextTag) -> Tuple[Any, str, Tuple[Tuple[int, int], ...]]:
        """Convert the data held in the StyledTextTag to a Python tuple."""
        return tag.serialize()

    def set_name(self, tag: StyledTextTag, name: Any) -> None:
        """Set the name of the StyledTextTag."""
        tag.set_name(name)

    def set_ranges(self, tag: StyledTextTag, ranges: List[Tuple[int, int]]) -> None:
        """Set the list of ranges."""
        tag.set_ranges(ranges)

    def set_value(self, tag: StyledTextTag, value: str) -> None:
        """Set the value of the StyledTextTag."""
        tag.set_value(value)

    def unserialize(self, tag: StyledTextTag, data: Tuple[Any, str, Tuple[Tuple[int, int], ...]]) -> None:
        """Convert the data held in a tuple back into the data in a StyledTextTag object."""
        tag.unserialize(data)