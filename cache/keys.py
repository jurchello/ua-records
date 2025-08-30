from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from uconstants.cache import (
    NAMESPACE_FORMSTATE,
    NAMESPACE_LISTS,
)
from uconstants.paths import CACHE_SUBDIR, USER_DATA_DIRNAME

if TYPE_CHECKING:
    from gramps.gen.db.base import DbReadBase


@dataclass(frozen=True)
class CacheKey:
    namespace: str
    type: str
    dbid: str
    version: str
    name: str

    def parts(self) -> tuple[str, str, str, str, str]:
        return self.namespace, self.type, self.dbid, self.version, self.name


def base_cache_dir() -> Path:
    try:
        from gramps.gen.const import USER_DATA  # pylint: disable=import-outside-toplevel

        root = Path(USER_DATA)
    except Exception:
        root = Path(os.path.expanduser("~"))
    return root.joinpath(USER_DATA_DIRNAME, CACHE_SUBDIR)


def path_for(base_dir: Path, key: CacheKey) -> Path:
    ns, t, dbid, ver, name = key.parts()
    return base_dir.joinpath(ns, t, dbid, ver, f"{name}.json")


def get_dbid(db: DbReadBase) -> str:
    f = getattr(db, "get_dbid", None)
    if callable(f):
        try:
            v = f()
            return str(v)
        except Exception:
            return str(id(db))
    return str(id(db))


def key_for_list(list_type: str, dbid: str, version: str = "v1", name: str = "all") -> CacheKey:
    return CacheKey(NAMESPACE_LISTS, list_type, dbid, version, name)


def key_for_formstate(form_type: str, dbid: str, name: str, version: str = "v1") -> CacheKey:
    return CacheKey(NAMESPACE_FORMSTATE, form_type, dbid, version, name)
