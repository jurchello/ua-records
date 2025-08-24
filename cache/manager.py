from __future__ import annotations

import shutil
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Tuple

from constants.cache import CODEC_JSON
from .keys import CacheKey, base_cache_dir, path_for
from .codecs import get_codec
from .store_file import CacheStoreFile, CacheMetadata, now_ts


class CacheStatus(str, Enum):
    HIT = "hit"
    STALE = "stale"
    MISS = "miss"
    ERROR = "error"


@dataclass
class CacheInfo:
    exists: bool
    bytes_size: int
    created_at: float
    updated_at: float
    ttl: int | None
    is_expired: bool
    codec: str
    schema_version: str | None
    path: Path


class CacheManager:
    def __init__(self, cache_dir: Path | None = None):
        self.base_dir = cache_dir or base_cache_dir()
        self.store = CacheStoreFile(self.base_dir)

    def write_full(
        self,
        key: CacheKey,
        value: Any,
        ttl_sec: int | None = None,
        codec: str = CODEC_JSON,
        schema_version: str | None = None,
    ) -> None:
        c = get_codec(codec)
        p = path_for(self.base_dir, key)
        ts = now_ts()
        payload = c.encode(value)
        meta = CacheMetadata(
            ttl=ttl_sec,
            codec=codec,
            schema_version=schema_version,
            created_at=ts,
            updated_at=ts,
        )
        self.store.write(p, payload, meta)

    def read(self, key: CacheKey, accept_stale: bool = False) -> Tuple[CacheStatus, Any]:
        p = path_for(self.base_dir, key)
        if not p.exists():
            return CacheStatus.MISS, None
        try:
            payload, meta = self.store.read(p)
            c = get_codec(meta.codec)
            expired = self.store.is_expired(meta)
            if expired and not accept_stale:
                return CacheStatus.MISS, None
            val = c.decode(payload)
            if expired:
                return CacheStatus.STALE, val
            return CacheStatus.HIT, val
        except Exception:
            return CacheStatus.ERROR, None

    def delete(self, key: CacheKey) -> bool:
        p = path_for(self.base_dir, key)
        return self.store.delete(p)

    def info(self, key: CacheKey) -> CacheInfo:
        p = path_for(self.base_dir, key)
        exists = p.exists()
        size, _ = self.store.stat(p)
        try:
            _, meta = self.store.read(p)
        except Exception:
            meta = CacheMetadata(
                ttl=None,
                codec=CODEC_JSON,
                schema_version=None,
                created_at=0.0,
                updated_at=0.0,
            )
        expired = self.store.is_expired(meta)
        return CacheInfo(
            exists=exists,
            bytes_size=size,
            created_at=meta.created_at,
            updated_at=meta.updated_at,
            ttl=meta.ttl,
            is_expired=expired,
            codec=meta.codec,
            schema_version=meta.schema_version,
            path=p,
        )

    def clear_namespace(self, namespace: str, dbid: str | None = None) -> int:
        root = self.base_dir.joinpath(namespace)
        if not root.exists():
            return 0
        if dbid is None:
            try:
                shutil.rmtree(root)
                return 1
            except Exception:
                return 0
        count = 0
        for tdir in root.iterdir():
            if not tdir.is_dir():
                continue
            dbdir = tdir.joinpath(dbid)
            if dbdir.exists():
                try:
                    shutil.rmtree(dbdir)
                    count += 1
                except Exception:
                    pass
        return count