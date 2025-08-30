from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Tuple

from uconstants.cache import CODEC_JSON, DEFAULT_METADATA, META_SUFFIX


@dataclass
class CacheMetadata:
    ttl: int | None
    codec: str
    schema_version: str | None
    created_at: float
    updated_at: float


def now_ts() -> float:
    return time.time()


def meta_path(path: Path) -> Path:
    return path.with_name(path.stem + META_SUFFIX)


def _as_int_or_none(v: Any) -> int | None:
    return v if isinstance(v, int) else None


def _as_float(v: Any, default: float = 0.0) -> float:
    if isinstance(v, (int, float)):
        return float(v)
    return default


def _as_str(v: Any, default: str) -> str:
    return v if isinstance(v, str) else default


def _as_str_or_none(v: Any) -> str | None:
    return v if isinstance(v, str) else None


class CacheStoreFile:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def ensure_dir(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, path: Path, payload: bytes, meta: CacheMetadata) -> None:
        self.ensure_dir(path)

        tmp = path.with_suffix(path.suffix + ".tmp")
        with open(tmp, "wb") as f:
            f.write(payload)
        os.replace(tmp, path)

        mpath = meta_path(path)
        mtmp = mpath.with_suffix(mpath.suffix + ".tmp")
        with open(mtmp, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "ttl": meta.ttl,
                    "codec": meta.codec,
                    "schema_version": meta.schema_version,
                    "created_at": meta.created_at,
                    "updated_at": meta.updated_at,
                },
                f,
                ensure_ascii=False,
                separators=(",", ":"),
            )
        os.replace(mtmp, mpath)

    def read(self, path: Path) -> Tuple[bytes, CacheMetadata]:
        with open(path, "rb") as f:
            data = f.read()

        mpath = meta_path(path)
        if mpath.exists():
            with open(mpath, "r", encoding="utf-8") as f:
                m: dict[str, Any] = json.load(f)
        else:
            m = dict(DEFAULT_METADATA)  # copy

        meta = CacheMetadata(
            ttl=_as_int_or_none(m.get("ttl")),
            codec=_as_str(m.get("codec"), CODEC_JSON),
            schema_version=_as_str_or_none(m.get("schema_version")),
            created_at=_as_float(m.get("created_at"), 0.0),
            updated_at=_as_float(m.get("updated_at"), 0.0),
        )
        return data, meta

    def delete(self, path: Path) -> bool:
        ok = False
        try:
            if path.exists():
                path.unlink()
                ok = True
        except Exception:
            ok = False
        try:
            m = meta_path(path)
            if m.exists():
                m.unlink()
        except Exception:
            pass
        return ok

    def stat(self, path: Path) -> Tuple[int, float]:
        if not path.exists():
            return 0, 0.0
        st = path.stat()
        return st.st_size, st.st_mtime

    def is_expired(self, meta: CacheMetadata, ts: float | None = None) -> bool:
        if meta.ttl is None:
            return False
        t = ts or now_ts()
        base = meta.updated_at or meta.created_at or 0.0
        return base + meta.ttl < t
