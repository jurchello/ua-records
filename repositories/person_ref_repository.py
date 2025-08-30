from __future__ import annotations

from gramps.gen.lib import PersonRef

from repositories.citation_base_repository import CitationBaseRepository


class PersonRefRepository(CitationBaseRepository):

    def get_relation(self, person_ref: PersonRef) -> str:
        return person_ref.get_relation()

    def get_reference_handle(self, person_ref: PersonRef) -> str:
        return person_ref.get_reference_handle()
