# Caching Library — Practical Guide

A practical, example‑driven guide to initialize, configure, and use the file‑based cache. The cache centers on **keys** (namespaced, versioned), **codecs** (serialization), **TTL/metadata**, and a thin **manager** that handles safe writes and reads.

> All names in this guide are neutral (project‑agnostic).

---

## TL;DR

```python
from pathlib import Path
from cache import key_for_list, CacheManager, CacheStatus

cm = CacheManager()  # or CacheManager(cache_dir=Path("/tmp/mycache"))
k = key_for_list(list_type="people", dbid="main-db", version="v1", name="all")

# Write for 24h
cm.write_full(k, ["P1", "P2", "P3"], ttl_sec=24*3600, codec="lists", schema_version="1.0")

# Read (reject stale by default)
status, value = cm.read(k)  # -> (CacheStatus.HIT, ["P1","P2","P3"]) or (MISS, None)

# Accept stale if you want a fallback while refreshing in background
status, value = cm.read(k, accept_stale=True)  # -> HIT|STALE|MISS
```

---

## What you get

- **Namespaced, versioned keys** → stable on‑disk layout: `namespace/type/dbid/version/name.json`.
- **Codecs** → pluggable encoders/decoders (`json`, `lists`, `formstate`, + custom).
- **TTL & metadata** → sidecar `*.meta.json` with `ttl`, `codec`, timestamps, schema version.
- **Safe writes** → atomic replace (`.tmp` file then `os.replace`).
- **Simple API** (`CacheManager`) → `write_full`, `read`, `delete`, `info`, `clear_namespace`.
- **Statuses** → `HIT`, `STALE`, `MISS`, `ERROR`.

---

## Key imports

```python
from cache import (
    CacheKey, key_for_list, key_for_formstate, get_dbid, base_cache_dir, path_for,
    CacheManager, CacheStatus, CacheInfo,
)
from uconstants.cache import (
    CODEC_JSON, CODEC_LISTS, CODEC_FORMSTATE,
    NAMESPACE_LISTS, NAMESPACE_FORMSTATE, NAMESPACE_MISC,
    CACHE_SCHEMA_VERSION,
)
```

---

## Concepts at a glance

### Key anatomy

A key is `(namespace, type, dbid, version, name)`:

```
<base_dir>/<namespace>/<type>/<dbid>/<version>/<name>.json
<base_dir>/<namespace>/<type>/<dbid>/<version>/<name>.meta.json
```

Built‑ins:
- `key_for_list(list_type, dbid, version="v1", name="all")`
- `key_for_formstate(form_type, dbid, name, version="v1")`

`dbid` can be derived from an object with `.get_dbid()` via `get_dbid(db)` (falls back to `id(db)` if absent).

### Namespaces (predefined)

- `lists` → generic lists (IDs, names, etc.)
- `formstate` → structured state payloads
- `misc` → anything else

You can ignore these and pass your own `namespace` by constructing `CacheKey` directly.

### Codecs

- `json` → raw JSON value (`dict/list/scalars`)
- `lists` → iterables of strings (coerced to `str`) → `["..."]`
- `formstate` → `dict[str, JSONValue]`

Register your own codec with `register_codec(...)` (see below).

### TTL & staleness

- Each write stores a TTL (seconds) in metadata.
- `read(key)` returns:
  - `HIT` if exists and not expired;
  - `STALE` if expired **and** you pass `accept_stale=True`;
  - `MISS` if missing or expired (when `accept_stale=False`);
  - `ERROR` if decoding/IO failed.
- Expiry is computed from `updated_at` (or `created_at` if `updated_at` is 0).

---

## Directory resolution

By default:

```python
from cache import base_cache_dir
base = base_cache_dir()  # resolves to user data dir (or home fallback)
```

- If the `gramps.gen.const.USER_DATA` symbol exists, that location is used as the root (the code checks and falls back safely).
- Override per manager: `CacheManager(cache_dir=Path("/custom/cache"))`.

Resulting layout example:

```
/custom/cache/
  lists/
    people/
      main-db/
        v1/
          all.json
          all.meta.json
```

---

## API Overview

### `CacheManager`

```python
cm = CacheManager()                              # or CacheManager(cache_dir=Path(...))
cm.write_full(key, value, ttl_sec=3600, codec="json", schema_version="1.0")
status, value = cm.read(key, accept_stale=False) # -> (HIT|MISS|STALE|ERROR, value-or-None)
ok = cm.delete(key)                              # -> True/False
info = cm.info(key)                              # -> CacheInfo(...)
removed = cm.clear_namespace("lists", dbid="main-db")
```

### `CacheStatus`

```
HIT | STALE | MISS | ERROR
```

### `CacheInfo`

```python
from dataclasses import asdict
ci = cm.info(key)
# ci.exists, ci.bytes_size, ci.created_at, ci.updated_at,
# ci.ttl, ci.is_expired, ci.codec, ci.schema_version, ci.path
```

---

## Writing & reading examples

### 1) Caching a list of IDs (24h)

```python
from cache import CacheManager, key_for_list
from uconstants.cache import CODEC_LISTS, CACHE_SCHEMA_VERSION

cm = CacheManager()
k = key_for_list("people", dbid="main-db", version="v1", name="all")
cm.write_full(k, ["P1","P2","P3"], ttl_sec=24*3600, codec=CODEC_LISTS, schema_version=CACHE_SCHEMA_VERSION)

status, val = cm.read(k)               # -> HIT
assert status.name == "HIT" and val == ["P1","P2","P3"]
```

### 2) Accept stale as fallback, then refresh

```python
status, val = cm.read(k, accept_stale=True)
if status == CacheStatus.MISS:
    val = recompute()                 # compute fresh
    cm.write_full(k, val, ttl_sec=3600, codec="lists", schema_version="1.0")
elif status == CacheStatus.STALE:
    trigger_background_refresh()      # schedule your own refresh; keep using `val` for now
```

### 3) Storing arbitrary JSON payload

```python
from uconstants.cache import CODEC_JSON
payload = {"page": 1, "items": [{"id": 1}, {"id": 2}]}
cm.write_full(k, payload, ttl_sec=600, codec=CODEC_JSON, schema_version="1.0")
```

### 4) Caching form state

```python
from cache import key_for_formstate
k2 = key_for_formstate("registration", dbid="main-db", name="user-123", version="v1")
state = {"step": 2, "fields": {"name": "Alice", "email": "a@example.com"}}
cm.write_full(k2, state, ttl_sec=3600, codec="formstate", schema_version="1.0")
status, state2 = cm.read(k2)
```

---

## Codecs (built‑ins & custom)

Built‑ins are already registered:

```python
from cache.codecs import get_codec, register_codec
from uconstants.cache import CODEC_JSON, CODEC_LISTS, CODEC_FORMSTATE

json_codec = get_codec(CODEC_JSON)         # encode/decode JSONValue
lists_codec = get_codec(CODEC_LISTS)       # encode/decode Iterable[str] <-> list[str]
formstate_codec = get_codec(CODEC_FORMSTATE)
```

### Register a custom codec

```python
from typing import Iterable
from cache.codecs import BaseCodec, register_codec

class IntListCodec(BaseCodec[Iterable[int], list[int]]):
    name = "intlist"
    def encode(self, obj: Iterable[int]) -> bytes:
        return ("[" + ",".join(str(i) for i in obj) + "]").encode("utf-8")
    def decode(self, data: bytes) -> list[int]:
        text = data.decode("utf-8").strip("[] \n\t")
        return [] if not text else [int(x) for x in text.split(",")]

register_codec(IntListCodec())
cm.write_full(k, [1,2,3], ttl_sec=60, codec="intlist", schema_version="1.0")
```

> If you need binary data or compression, implement a codec that returns/accepts `bytes`—the manager stores payloads verbatim.

---

## Metadata & files

Each payload file has a **sidecar** JSON file with metadata:

```json
{
  "ttl": 3600,
  "codec": "lists",
  "schema_version": "1.0",
  "created_at": 1724575200.0,
  "updated_at": 1724575200.0
}
```

File naming helpers (used internally by the manager):

```python
from cache.store_file import meta_path
mpath = meta_path(Path("/.../name.json"))  # -> /.../name.meta.json
```

---

## Ready‑to‑use “autoinit” modules (pick one)

Drop any of these as `cache/autoinit.py` (or similar) and import it early. Each variant exposes a ready `cm: CacheManager` and optional helpers.

### 1) Default local cache (files only, permissive TTL use)

```python
# cache/autoinit.py
from __future__ import annotations
from cache import CacheManager

cm = CacheManager()  # base dir resolved automatically
__all__ = ["cm"]
```

### 2) Strict TTL (never accept stale; helpers)

```python
# cache/autoinit.py
from __future__ import annotations
from cache import CacheManager, CacheStatus

cm = CacheManager()

def get_strict(key):
    status, val = cm.read(key, accept_stale=False)
    if status == CacheStatus.HIT:
        return val
    return None  # caller decides how to recompute

__all__ = ["cm", "get_strict"]
```

### 3) Stale‑OK fallback with “should refresh” flag

```python
# cache/autoinit.py
from __future__ annotations
from typing import Tuple, Any
from cache import CacheManager, CacheStatus

cm = CacheManager()

def get_with_refresh_hint(key) -> Tuple[Any | None, bool]:
    status, val = cm.read(key, accept_stale=True)
    if status == CacheStatus.MISS:
        return None, True    # definitely recompute
    if status == CacheStatus.STALE:
        return val, True     # can use stale value, but should refresh
    return val, False        # fresh

__all__ = ["cm", "get_with_refresh_hint"]
```

### 4) Custom codecs & schema versioning baked in

```python
# cache/autoinit.py
from __future__ annotations
from dataclasses import asdict, is_dataclass
import json
from typing import Any
from cache import CacheManager
from cache.codecs import BaseCodec, register_codec
from uconstants.cache import CACHE_SCHEMA_VERSION

class DataclassJSONCodec(BaseCodec[Any, Any]):
    name = "dataclass_json"
    def encode(self, obj: Any) -> bytes:
        if is_dataclass(obj):
            obj = asdict(obj)
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    def decode(self, data: bytes) -> Any:
        return json.loads(data.decode("utf-8"))

register_codec(DataclassJSONCodec())
cm = CacheManager()
DEFAULT_SCHEMA = CACHE_SCHEMA_VERSION  # use consistently across writes
__all__ = ["cm", "DEFAULT_SCHEMA"]
```

---

## Patterns & recipes

### Replace whole payload atomically

`write_full(...)` always writes to a temp file and atomically replaces the target. You can repeatedly overwrite the same key to update the cache without partial writes.

### Key versioning

Use `version="v2"` in the key when you change your payload shape. Also set a new `schema_version` in metadata to aid migrations.

### Clearing cache buckets

```python
from uconstants.cache import NAMESPACE_LISTS

# wipe entire namespace
cm.clear_namespace(NAMESPACE_LISTS)

# wipe all types within a namespace but only for a specific dbid
cm.clear_namespace(NAMESPACE_LISTS, dbid="main-db")
```

### Mixing codecs per channel/type

You can store different payloads for the same logical data by using distinct keys and codecs (e.g., a compact integer list vs. verbose JSON).

---

## Error handling & troubleshooting

- `CacheStatus.ERROR` on `read` usually means the codec failed to decode or the meta file was malformed. Consider catching and rewriting the entry.
- `MISS` after expiry: pass `accept_stale=True` if you want to serve stale values while recomputing.
- No files created? Ensure the process can create the base dir (or pass `cache_dir=...`).
- Wrong type loaded? Verify you passed the correct **codec** on write (codecs are stored in metadata and used during read).

---

## Minimal tests (pseudo)

```python
k = key_for_list("demo", "db", "v1", "all")
cm.write_full(k, ["a","b"], ttl_sec=1, codec="lists", schema_version="1.0")
status, v = cm.read(k); assert status.name == "HIT" and v == ["a","b"]
import time; time.sleep(1.1)
status, v = cm.read(k); assert status.name in {"MISS","HIT"}  # depends on clock/FS resolution
status, v = cm.read(k, accept_stale=True); assert status.name in {"STALE","HIT"}
assert cm.delete(k) in {True, False}
info = cm.info(k); assert info.path.name.endswith(".json")
```

---

## License

This guide documents a neutral, file‑based caching interface. See your project’s LICENSE for distribution terms.
