# pylint: disable=duplicate-code
from __future__ import annotations

import traceback
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from lookups.people_scan import PeopleScanner
from repositories.event_repository import EventRepository
from repositories.person_repository import PersonRepository

if TYPE_CHECKING:
    from gramps.gen.db.base import DbReadBase


# =========================
#   Runtime DB bootstrap
# =========================

_STATE: dict[str, Any] = {
    "runtime_db": None,  # type: Optional[DbReadBase]
}


def set_runtime_db(db: DbReadBase) -> None:
    """Register active Gramps DB for options providers."""
    _STATE["runtime_db"] = db


set_runtime_lookup = set_runtime_db


def _active_db(explicit_db: DbReadBase | None = None) -> DbReadBase:
    db = explicit_db or _STATE.get("runtime_db")
    if db is None:
        raise RuntimeError(
            "No active Gramps DB is set. Call configs.options.set_runtime_db(db) "
            "during plugin init, or pass db=... when calling options providers."
        )
    return db


# =========================
#        Caching
# =========================

_dynamic_options_cache: dict[tuple[str, str | int], list[str]] = {}
_scan_cache: dict[tuple[str, str | int], dict[str, set[str]]] = {}


def _db_cache_key(db: DbReadBase, name: str) -> tuple[str, str | int]:
    get_id = getattr(db, "get_dbid", None)
    if callable(get_id):
        try:
            raw = get_id()
        except Exception:
            raw = None
        if isinstance(raw, (str, int)):
            db_id: str | int = raw
        else:
            db_id = str(raw) if raw is not None else id(db)
        return (name, db_id)
    return (name, id(db))


def cached_provider(
    fn: Callable[[DbReadBase], list[str]],
) -> Callable[..., list[str]]:
    name = fn.__name__

    def wrapper(*args: Any, **kwargs: Any) -> list[str]:
        db = kwargs.pop("db", None)
        if db is None and args:
            db = args[0]
        db = _active_db(db)

        key = _db_cache_key(db, name)
        if key in _dynamic_options_cache:
            return _dynamic_options_cache[key]

        try:
            res = fn(db) or []
        except Exception:
            traceback.print_exc()
            res = []

        if isinstance(res, dict):
            res = []
        else:
            res = list(res)

        _dynamic_options_cache[key] = res
        return res

    wrapper.__wrapped__ = fn
    wrapper.__name__ = name
    return wrapper


# =========================
#     People scan core
# =========================


def _people_scan(db: DbReadBase) -> dict[str, set[str]]:
    key = _db_cache_key(db, "_people_scan_dict")
    cached = _scan_cache.get(key)
    if cached is not None:
        return cached

    try:
        result = PeopleScanner(PersonRepository(db), EventRepository(db)).scan()
        if not isinstance(result, dict):
            result = {}
    except Exception:
        result = {}

    for k in (
        "man_castes",
        "woman_castes",
        "all_castes",
        "man_given",
        "woman_given",
        "all_given",
        "man_surnames",
        "woman_surnames",
        "all_surnames",
        "man_military_ranks",
        "man_occupations",
        "woman_occupations",
        "all_occupations",
        "all_death_causes",
    ):
        result.setdefault(k, set())

    _scan_cache[key] = result
    return result


# =========================
#       Providers (lists)
# =========================


@cached_provider
def man_castes(db: DbReadBase) -> list[str]:
    return sorted(_people_scan(db)["man_castes"])


@cached_provider
def woman_castes(db: DbReadBase) -> list[str]:
    return sorted(_people_scan(db)["woman_castes"])


@cached_provider
def all_castes(db: DbReadBase) -> list[str]:
    return sorted(_people_scan(db)["all_castes"])


@cached_provider
def man_given(db: DbReadBase) -> list[str]:
    return sorted(_people_scan(db)["man_given"])


@cached_provider
def woman_given(db: DbReadBase) -> list[str]:
    return sorted(_people_scan(db)["woman_given"])


@cached_provider
def all_given(db: DbReadBase) -> list[str]:
    return sorted(_people_scan(db)["all_given"])


@cached_provider
def man_surnames(db: DbReadBase) -> list[str]:
    return sorted(_people_scan(db)["man_surnames"])


@cached_provider
def woman_surnames(db: DbReadBase) -> list[str]:
    return sorted(_people_scan(db)["woman_surnames"])


@cached_provider
def all_surnames(db: DbReadBase) -> list[str]:
    return sorted(_people_scan(db)["all_surnames"])


@cached_provider
def man_military_ranks(db: DbReadBase) -> list[str]:
    return sorted(_people_scan(db)["man_military_ranks"])


@cached_provider
def all_death_causes(db: DbReadBase) -> list[str]:
    raw_causes = _people_scan(db)["all_death_causes"]
    try:
        # from forms.death.config import death_causes_blacklist
        death_causes_blacklist = set()  # TODO: implement death module
    except Exception:
        death_causes_blacklist = []
    filtered = {
        cause for cause in raw_causes if not any(blk.lower() in cause.lower() for blk in death_causes_blacklist)
    }
    return sorted(filtered)


OCCUPATIONS_BLACKLIST = [
    "Occupation of",
]


@cached_provider
def all_occupations(db: DbReadBase) -> list[str]:
    raw = _people_scan(db)["all_occupations"]
    filtered = {occ for occ in raw if not any(blk.lower() in occ.lower() for blk in OCCUPATIONS_BLACKLIST)}
    return sorted(filtered)


@cached_provider
def man_occupations(db: DbReadBase) -> list[str]:
    raw = _people_scan(db)["man_occupations"]
    filtered = {occ for occ in raw if not any(blk.lower() in occ.lower() for blk in OCCUPATIONS_BLACKLIST)}
    return sorted(filtered)


@cached_provider
def woman_occupations(db: DbReadBase) -> list[str]:
    raw = _people_scan(db)["woman_occupations"]
    filtered = {occ for occ in raw if not any(blk.lower() in occ.lower() for blk in OCCUPATIONS_BLACKLIST)}
    return sorted(filtered)


def clear_options_cache() -> None:
    """Clear both list and scan caches."""
    _dynamic_options_cache.clear()
    _scan_cache.clear()
