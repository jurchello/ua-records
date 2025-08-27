from __future__ import annotations
from typing import Any, Callable, Optional
import threading
from cache import CacheManager, key_for_list, get_dbid
from cache import CacheStatus
from uconstants.cache import CODEC_LISTS, CACHE_SCHEMA_VERSION
from repositories.base_repository import BaseRepository
from repositories.person_repository import PersonRepository
from repositories.event_repository import EventRepository
from .people_scan import PeopleScanner

_RUNTIME_DB: Optional[Any] = None
_cm = CacheManager()
_options_cache: dict[tuple[str, str | int], list[str] | dict[str, set[str]]] = {}
_refresh_lock = threading.Lock()
_refresh_timer: Optional[threading.Timer] = None

TTL_SEC = 24 * 3600
VERSION = "v1"
LIST_TYPE = "people_options"

def set_runtime_db(db: Any) -> None:
    global _RUNTIME_DB
    _RUNTIME_DB = db

def _active_db(db: Any | None = None) -> Any:
    x = db or _RUNTIME_DB
    if x is None:
        raise RuntimeError("No active DB set. Call set_runtime_db(db).")
    return x

def _db_key(db: Any, name: str) -> tuple[str, str | int]:
    try:
        return name, _safe_dbid(db)
    except Exception:
        return name, id(db)

def _safe_dbid(db: Any) -> str | int:
    try:
        return get_dbid(db)
    except Exception:
        return id(db)

def _key(name: str, db: Any) -> Any:
    return key_for_list(list_type=LIST_TYPE, dbid=_safe_dbid(db), version=VERSION, name=name)

def _cached(fn: Callable[[Any], list[str] | dict[str, set[str]]]) -> Callable[..., list[str]]:
    name = fn.__name__
    def wrapper(*args: Any, **kwargs: Any) -> list[str]:
        db = kwargs.pop("db", None) or (args[0] if args else None)
        db = _active_db(db)
        k = _db_key(db, name)
        if k in _options_cache:
            val = _options_cache[k]
            return list(val) if not isinstance(val, dict) else []
        status, val = _cm.read(_key(name, db), accept_stale=True)
        if status in (CacheStatus.HIT, CacheStatus.STALE) and isinstance(val, list):
            _options_cache[k] = val
            return list(val)
        res = fn(db) or []
        if isinstance(res, dict):
            return []
        _cm.write_full(_key(name, db), list(res), ttl_sec=TTL_SEC, codec=CODEC_LISTS, schema_version=CACHE_SCHEMA_VERSION)
        _options_cache[k] = list(res)
        return list(res)
    wrapper.__name__ = name
    return wrapper

def _scan(db: Any) -> dict[str, set[str]]:
    pr = PersonRepository(db)
    er = EventRepository(db)
    return PeopleScanner(pr, er).scan()

def _ensure_scan_cached(db: Any) -> dict[str, set[str]]:
    name = "_PEOPLE_SCAN"
    kdict = _db_key(db, name)
    if kdict in _options_cache and isinstance(_options_cache[kdict], dict):
        return _options_cache[kdict]  # type: ignore[return-value]
    status, val = _cm.read(_key(name, db), accept_stale=True)
    if status in (CacheStatus.HIT, CacheStatus.STALE) and isinstance(val, list):
        _options_cache[kdict] = {}
        return {}
    data = _scan(db)
    _options_cache[kdict] = data
    return data

def _from_scan(db: Any, field: str) -> list[str]:
    s = _ensure_scan_cached(db)
    return sorted(s.get(field, set()))

@_cached
def MAN_CASTES(db: Any) -> list[str]:
    return _from_scan(db, "man_castes")

@_cached
def WOMAN_CASTES(db: Any) -> list[str]:
    return _from_scan(db, "woman_castes")

@_cached
def ALL_CASTES(db: Any) -> list[str]:
    return _from_scan(db, "all_castes")

@_cached
def MAN_GIVEN(db: Any) -> list[str]:
    return _from_scan(db, "man_given")

@_cached
def WOMAN_GIVEN(db: Any) -> list[str]:
    return _from_scan(db, "woman_given")

@_cached
def ALL_GIVEN(db: Any) -> list[str]:
    return _from_scan(db, "all_given")

@_cached
def MAN_SURNAMES(db: Any) -> list[str]:
    return _from_scan(db, "man_surnames")

@_cached
def WOMAN_SURNAMES(db: Any) -> list[str]:
    return _from_scan(db, "woman_surnames")

@_cached
def ALL_SURNAMES(db: Any) -> list[str]:
    return _from_scan(db, "all_surnames")

@_cached
def MAN_MILITARY_RANKS(db: Any) -> list[str]:
    return _from_scan(db, "man_military_ranks")

@_cached
def ALL_DEATH_CAUSES(db: Any) -> list[str]:
    raw = set(_from_scan(db, "all_death_causes"))
    try:
        from forms.death.config import DEATH_CAUSES_BLACKLIST
    except Exception:
        DEATH_CAUSES_BLACKLIST = []
    return sorted(x for x in raw if not any(b.lower() in x.lower() for b in DEATH_CAUSES_BLACKLIST))

OCCUPATIONS_BLACKLIST = ["Occupation of"]

@_cached
def ALL_OCCUPATIONS(db: Any) -> list[str]:
    raw = set(_from_scan(db, "all_occupations"))
    return sorted(x for x in raw if not any(b.lower() in x.lower() for b in OCCUPATIONS_BLACKLIST))

@_cached
def MAN_OCCUPATIONS(db: Any) -> list[str]:
    raw = set(_from_scan(db, "man_occupations"))
    return sorted(x for x in raw if not any(b.lower() in x.lower() for b in OCCUPATIONS_BLACKLIST))

@_cached
def WOMAN_OCCUPATIONS(db: Any) -> list[str]:
    raw = set(_from_scan(db, "woman_occupations"))
    return sorted(x for x in raw if not any(b.lower() in x.lower() for b in OCCUPATIONS_BLACKLIST))

def clear_options_cache() -> None:
    _options_cache.clear()

def force_refresh(db: Any | None = None) -> None:
    x = _active_db(db)
    clear_options_cache()
    data = _scan(x)
    for name, field in [
        ("MAN_CASTES","man_castes"),("WOMAN_CASTES","woman_castes"),("ALL_CASTES","all_castes"),
        ("MAN_GIVEN","man_given"),("WOMAN_GIVEN","woman_given"),("ALL_GIVEN","all_given"),
        ("MAN_SURNAMES","man_surnames"),("WOMAN_SURNAMES","woman_surnames"),("ALL_SURNAMES","all_surnames"),
        ("MAN_MILITARY_RANKS","man_military_ranks"),
        ("ALL_DEATH_CAUSES","all_death_causes"),
        ("ALL_OCCUPATIONS","all_occupations"),("MAN_OCCUPATIONS","man_occupations"),("WOMAN_OCCUPATIONS","woman_occupations"),
    ]:
        vals = sorted(data.get(field, set()))
        _cm.write_full(_key(name, x), vals, ttl_sec=TTL_SEC, codec=CODEC_LISTS, schema_version=CACHE_SCHEMA_VERSION)

def schedule_refresh_after_save(db: Any | None = None, delay_sec: int = 3) -> None:
    x = _active_db(db)
    global _refresh_timer
    with _refresh_lock:
        if _refresh_timer:
            _refresh_timer.cancel()
        def worker():
            try:
                force_refresh(x)
            except Exception:
                pass
        _refresh_timer = threading.Timer(delay_sec, worker)
        _refresh_timer.daemon = True
        _refresh_timer.start()