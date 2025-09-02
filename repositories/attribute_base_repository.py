from __future__ import annotations

from typing import List

from gramps.gen.lib import Attribute

from repositories.attribute_root_base_repository import AttributeRootBaseRepository


class AttributeBaseRepository(AttributeRootBaseRepository):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

