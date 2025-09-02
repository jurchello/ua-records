from __future__ import annotations
from collections import defaultdict
from typing import Any, List, Tuple
from gramps.gen.db.txn import DbTxn

class DbTxnRepository(defaultdict):

    def add(self, obj, obj_type: int, trans_type: int, handle: str, old_data: Tuple[Any, ...], new_data: Tuple[Any, ...]) -> None:
        obj.add(obj_type, trans_type, handle, old_data, new_data)

    def batch(self, obj) -> Any:
        return obj.batch

    def commitdb(self, obj) -> Any:
        return obj.commitdb

    def db(self, obj) -> Any:
        return obj.db

    def first(self, obj) -> Any:
        return obj.first

    def get_description(self, obj) -> str:
        return obj.get_description()

    def get_recnos(self, obj, reverse: bool = False) -> List[Any] | range:
        return obj.get_recnos(reverse=reverse)

    def get_record(self, obj, recno: int) -> Tuple[int, str, Tuple[Any, ...]]:
        return obj.get_record(recno)

    def last(self, obj) -> Any:
        return obj.last

    def msg(self, obj) -> Any:
        return obj.msg

    def set_description(self, obj, msg: str) -> None:
        obj.set_description(msg)

    def timestamp(self, obj) -> Any:
        return obj.timestamp