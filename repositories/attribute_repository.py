from __future__ import annotations

from typing import Any, Dict, List, Sequence, Tuple

from gramps.gen.lib import Attribute

from repositories.attribute_root_repository import AttributeRootRepository
from repositories.citation_base_repository import CitationBaseRepository
from repositories.note_base_repository import NoteBaseRepository

class AttributeRepository(
    AttributeRootRepository,
    CitationBaseRepository,
    NoteBaseRepository,
):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_referenced_handles(self, attribute: Attribute) -> List[Tuple[str, str]]:
        return attribute.get_referenced_handles()

    def get_schema(self) -> Dict[str, Any]:
        return Attribute.get_schema()

    def merge(self, attribute: Attribute, acquisition: Attribute) -> None:
        attribute.merge(acquisition)

    def serialize(self, attribute: Attribute) -> Sequence[Any]:
        return attribute.serialize()

    def unserialize(self, attribute: Attribute, data: Sequence[Any]) -> None:
        attribute.unserialize(tuple(data))