from __future__ import annotations
import types
import time
import pytest

# These tests assume your project has ua_records.lookups.providers implemented
# as discussed. We monkeypatch PeopleScanner and the CacheManager location
# to use a temporary directory so tests are hermetic.

@pytest.fixture(autouse=True)
def patch_cache_dir(tmp_path, monkeypatch):
    import lookups.providers as lookups
    from cache import CacheManager
    lookups._cm = CacheManager(cache_dir=tmp_path)  # type: ignore[attr-defined]
    lookups.clear_options_cache()
    yield

@pytest.fixture
def fake_db():
    class DB:
        def get_dbid(self): return "test-db"
    return DB()

@pytest.fixture
def patch_scanner(monkeypatch):
    import lookups.providers as lookups
    class FakeScanner:
        def __init__(self, *a, **k): pass
        def scan(self):
            return {
                "man_castes": {"козак"},
                "woman_castes": {"міщанка"},
                "all_castes": {"козак","міщанка"},
                "man_given": {"Іван"},
                "woman_given": {"Марія"},
                "all_given": {"Іван","Марія"},
                "man_surnames": {"Петренко"},
                "woman_surnames": {"Іванчук"},
                "all_surnames": {"Петренко","Іванчук"},
                "man_military_ranks": {"рядовий"},
                "man_occupations": {"коваль"},
                "woman_occupations": {"швачка"},
                "all_occupations": {"коваль","швачка"},
                "all_death_causes": {"туберкульоз легень","старість"},
            }
    monkeypatch.setattr(lookups, "PeopleScanner", FakeScanner)
    return FakeScanner

def test_lists_are_returned_and_sorted(fake_db, patch_scanner, monkeypatch):
    import lookups.providers as lookups
    lookups.set_runtime_db(fake_db)
    assert lookups.MAN_SURNAMES() == ["Петренко"]
    assert lookups.WOMAN_SURNAMES() == ["Іванчук"]
    assert lookups.ALL_SURNAMES() == ["Іванчук","Петренко"]
    assert lookups.MAN_GIVEN() == ["Іван"]
    assert lookups.WOMAN_GIVEN() == ["Марія"]
    assert lookups.ALL_GIVEN() == ["Іван","Марія"]
    assert lookups.MAN_CASTES() == ["козак"]
    assert lookups.WOMAN_CASTES() == ["міщанка"]
    assert lookups.ALL_CASTES() == ["козак","міщанка"]
    assert lookups.MAN_MILITARY_RANKS() == ["рядовий"]
    assert lookups.ALL_OCCUPATIONS() == ["коваль","швачка"]
    assert lookups.MAN_OCCUPATIONS() == ["коваль"]
    assert lookups.WOMAN_OCCUPATIONS() == ["швачка"]
    assert sorted(lookups.ALL_DEATH_CAUSES()) == ["старість","туберкульоз легень"]

def test_cache_hit_and_stale_flow(fake_db, patch_scanner, tmp_path):
    import lookups.providers as lookups
    lookups.set_runtime_db(fake_db)
    first = lookups.MAN_SURNAMES()
    assert first == ["Петренко"]
    # Force-refresh writes fresh values (HIT)
    lookups.force_refresh()
    second = lookups.MAN_SURNAMES()
    assert second == ["Петренко"]
    # Simulate TTL expiry by rewriting meta with tiny ttl
    k = lookups._key("MAN_SURNAMES", fake_db)  # type: ignore[attr-defined]
    info = lookups._cm.info(k)  # type: ignore[attr-defined]
    meta_path = info.path.with_suffix(".meta.json")
    meta = meta_path.read_text(encoding="utf-8")
    meta = meta.replace('"ttl": 86400', '"ttl": 0')
    meta_path.write_text(meta, encoding="utf-8")
    stale = lookups.MAN_SURNAMES()
    assert stale == ["Петренко"]  # still served due to accept_stale=True
