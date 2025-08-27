from __future__ import annotations
from typing import Any
from gramps.gen.lib import ChildRef

from repositories.base_repository import BaseRepository


class ChildRefRepository(BaseRepository):
    
    def get_reference_handle(self, child_ref: ChildRef) -> str:
        return child_ref.get_reference_handle()
    
    def get_father_relation(self, child_ref: ChildRef) -> Any:
        return child_ref.get_father_relation()
    
    def get_mother_relation(self, child_ref: ChildRef) -> Any:
        return child_ref.get_mother_relation()
    
    def set_reference_handle(self, child_ref: ChildRef, handle: str) -> None:
        child_ref.set_reference_handle(handle)
    
    def set_father_relation(self, child_ref: ChildRef, relation: Any) -> None:
        child_ref.set_father_relation(relation)
    
    def set_mother_relation(self, child_ref: ChildRef, relation: Any) -> None:
        child_ref.set_mother_relation(relation)