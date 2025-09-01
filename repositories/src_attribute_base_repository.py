from __future__ import annotations

from repositories.attribute_root_base_repository import AttributeRootBaseRepository


class SrcAttributeBaseRepository(AttributeRootBaseRepository):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)
