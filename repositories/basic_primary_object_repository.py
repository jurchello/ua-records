from __future__ import annotations
from gramps.gen.lib.primaryobj import BasicPrimaryObject

from repositories.table_object_repository import TableObjectRepository


class BasicPrimaryObjectRepository(TableObjectRepository):
    
    def get_gramps_id(self, obj: BasicPrimaryObject) -> str:
        return obj.get_gramps_id()