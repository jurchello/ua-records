from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Any, Callable, Optional

from cache import CacheManager, CacheStatus, get_dbid, key_for_list
from repositories.event_repository import EventRepository
from repositories.person_repository import PersonRepository
from uconstants.cache import CACHE_SCHEMA_VERSION, CODEC_LISTS

from .people_scan import PeopleScanner

if TYPE_CHECKING:
    from gramps.gen.db.base import DbReadBase


# -----------------------------
# Internal mutable state holder
# -----------------------------
_STATE: dict[str, Any] = {
    "runtime_db": None,  # type: Optional[DbReadBase]
    "refresh_timer": None,  # type: Optional[threading.Timer]
}

_cm = CacheManager()
_options_cache: dict[tuple[str, str], list[str] | dict[str, set[str]]] = {}
_refresh_lock = threading.Lock()

TTL_SEC = 24 * 3600
VERSION = "v1"
LIST_TYPE = "people_options"


def set_runtime_db(db: DbReadBase) -> None:
    """Register active DB for providers’ functions (no globals)."""
    _STATE["runtime_db"] = db


def _active_db(db: DbReadBase | None = None) -> DbReadBase:
    x = db or _STATE.get("runtime_db")
    if x is None:
        raise RuntimeError("No active DB set. Call set_runtime_db(db).")
    return x


def _db_key(db: DbReadBase, name: str) -> tuple[str, str]:
    return name, _safe_dbid(db)


def _safe_dbid(db: DbReadBase) -> str:
    try:
        val = get_dbid(db)
    except Exception:
        val = id(db)
    return str(val)


def _key(name: str, db: DbReadBase) -> Any:
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
        _cm.write_full(
            _key(name, db),
            list(res),
            ttl_sec=TTL_SEC,
            codec=CODEC_LISTS,
            schema_version=CACHE_SCHEMA_VERSION,
        )
        _options_cache[k] = list(res)
        return list(res)

    wrapper.__name__ = name
    return wrapper


def _scan(db: DbReadBase) -> dict[str, set[str]]:
    pr = PersonRepository(db)
    er = EventRepository(db)
    return PeopleScanner(pr, er).scan()


def _ensure_scan_cached(db: DbReadBase) -> dict[str, set[str]]:
    name = "_people_scan"
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


def _from_scan(db: DbReadBase, field: str) -> list[str]:
    s = _ensure_scan_cached(db)
    return sorted(s.get(field, set()))


@_cached
def man_castes(db: DbReadBase) -> list[str]:
    return _from_scan(db, "man_castes")


@_cached
def woman_castes(db: DbReadBase) -> list[str]:
    return _from_scan(db, "woman_castes")


@_cached
def all_castes(db: DbReadBase) -> list[str]:
    return _from_scan(db, "all_castes")


@_cached
def man_given(db: DbReadBase) -> list[str]:
    return _from_scan(db, "man_given")


@_cached
def woman_given(db: DbReadBase) -> list[str]:
    return _from_scan(db, "woman_given")


@_cached
def all_given(db: DbReadBase) -> list[str]:
    return _from_scan(db, "all_given")


@_cached
def man_surnames(db: DbReadBase) -> list[str]:
    return _from_scan(db, "man_surnames")


@_cached
def woman_surnames(db: DbReadBase) -> list[str]:
    return _from_scan(db, "woman_surnames")


@_cached
def all_surnames(db: DbReadBase) -> list[str]:
    return _from_scan(db, "all_surnames")


@_cached
def man_military_ranks(db: DbReadBase) -> list[str]:
    return _from_scan(db, "man_military_ranks")


@_cached
def all_death_causes(db: DbReadBase) -> list[str]:
    raw = set(_from_scan(db, "all_death_causes"))
    try:
        # from forms.death.config import death_causes_blacklist
        death_causes_blacklist = set()  # TODO: implement death module
    except Exception:
        death_causes_blacklist = []
    return sorted(x for x in raw if not any(b.lower() in x.lower() for b in death_causes_blacklist))


OCCUPATIONS_BLACKLIST = ["Occupation of"]


@_cached
def all_occupations(db: DbReadBase) -> list[str]:
    raw = set(_from_scan(db, "all_occupations"))
    return sorted(x for x in raw if not any(b.lower() in x.lower() for b in OCCUPATIONS_BLACKLIST))


@_cached
def man_occupations(db: DbReadBase) -> list[str]:
    raw = set(_from_scan(db, "man_occupations"))
    return sorted(x for x in raw if not any(b.lower() in x.lower() for b in OCCUPATIONS_BLACKLIST))


@_cached
def woman_occupations(db: DbReadBase) -> list[str]:
    raw = set(_from_scan(db, "woman_occupations"))
    return sorted(x for x in raw if not any(b.lower() in x.lower() for b in OCCUPATIONS_BLACKLIST))


def clear_options_cache() -> None:
    _options_cache.clear()


def force_refresh(db: DbReadBase | None = None) -> None:
    x = _active_db(db)
    clear_options_cache()
    data = _scan(x)
    for name, field in [
        ("man_castes", "man_castes"),
        ("woman_castes", "woman_castes"),
        ("all_castes", "all_castes"),
        ("man_given", "man_given"),
        ("woman_given", "woman_given"),
        ("all_given", "all_given"),
        ("man_surnames", "man_surnames"),
        ("woman_surnames", "woman_surnames"),
        ("all_surnames", "all_surnames"),
        ("man_military_ranks", "man_military_ranks"),
        ("all_death_causes", "all_death_causes"),
        ("all_occupations", "all_occupations"),
        ("man_occupations", "man_occupations"),
        ("woman_occupations", "woman_occupations"),
    ]:
        vals = sorted(data.get(field, set()))
        _cm.write_full(
            _key(name, x),
            vals,
            ttl_sec=TTL_SEC,
            codec=CODEC_LISTS,
            schema_version=CACHE_SCHEMA_VERSION,
        )


def schedule_refresh_after_save(db: DbReadBase | None = None, delay_sec: int = 3) -> None:
    """
    Schedule delayed cache rebuild after save. Re-uses a single timer per process.
    """
    x = _active_db(db)
    with _refresh_lock:
        prev: Optional[threading.Timer] = _STATE.get("refresh_timer")
        if prev:
            prev.cancel()

        def worker():
            try:
                force_refresh(x)
            except Exception:
                pass

        timer = threading.Timer(delay_sec, worker)
        timer.daemon = True
        timer.start()
        _STATE["refresh_timer"] = timer
